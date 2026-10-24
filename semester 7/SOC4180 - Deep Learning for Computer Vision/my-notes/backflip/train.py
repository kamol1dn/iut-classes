"""Train the G1 to backflip with PPO, and WATCH it learn in a live window.

    uv run --project ../../labs/soc4180 python train.py
    uv run --project ../../labs/soc4180 python train.py --steps 80e6 --envs 96 --workers 15
    uv run --project ../../labs/soc4180 python train.py --resume runs/latest
    uv run --project ../../labs/soc4180 python train.py --no-viewer

Training runs --envs robots spread over --workers processes (batched_vec.py). A
separate thread replays the current policy (the mean action, no exploration
noise) in the MuJoCo window, one attempt after another, in slow motion, with the
network refreshed after every update. Closing the window does not stop training.

The terminal prints, per update: steps so far, speed, mean episode return,
how far the robots rotate (mean and best, in degrees) and how many landed.
Checkpoints go to runs/latest (overwritten) and runs/best (best landing rate).
"""

from __future__ import annotations

import argparse
import functools
import os
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def _build_env(seed, torque_scale):
    from backflip_env import G1BackflipEnv
    env = G1BackflipEnv(torque_scale=torque_scale)
    env.reset(seed=seed)
    return env


def make_env(seed, torque_scale):
    # a partial of a module-level function pickles; a closure does not (Windows spawns workers)
    return functools.partial(_build_env, seed, torque_scale)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=float, default=60e6)
    ap.add_argument("--envs", type=int, default=96, help="robots training in parallel")
    ap.add_argument("--workers", type=int, default=max(2, (os.cpu_count() or 4) - 1))
    ap.add_argument("--slowmo", type=float, default=2.0, help="demo playback is this many times slower")
    ap.add_argument("--torque-scale", type=float, default=1.0)
    ap.add_argument("--resume", type=str, default=None)
    ap.add_argument("--no-viewer", action="store_true")
    args = ap.parse_args()

    import torch
    from stable_baselines3 import PPO
    from stable_baselines3.common.callbacks import BaseCallback
    from stable_baselines3.common.vec_env import VecMonitor, VecNormalize
    from backflip_env import G1BackflipEnv
    from batched_vec import BatchedSubprocVecEnv
    torch.set_num_threads(4)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    venv = VecMonitor(BatchedSubprocVecEnv(
        [make_env(1000 + i, args.torque_scale) for i in range(args.envs)], args.workers))
    runs = HERE / "runs"
    runs.mkdir(exist_ok=True)
    if args.resume:
        venv = VecNormalize.load(str(Path(args.resume) / "vecnorm.pkl"), venv)
        agent = PPO.load(str(Path(args.resume) / "model.zip"), env=venv, device=device)
        print(f"resumed from {args.resume} at {agent.num_timesteps:,} steps")
    else:
        venv = VecNormalize(venv, norm_obs=True, norm_reward=True, clip_obs=10.0, gamma=0.99)
        agent = PPO(
            "MlpPolicy", venv, device=device, seed=0, verbose=0,
            n_steps=128, batch_size=args.envs * 32, n_epochs=5, learning_rate=3e-4,
            gamma=0.99, gae_lambda=0.95, clip_range=0.2, ent_coef=0.0, max_grad_norm=1.0,
            policy_kwargs=dict(net_arch=dict(pi=[512, 256, 128], vf=[512, 256, 128]),
                               activation_fn=torch.nn.ELU, log_std_init=-0.7),
        )
    per_update = agent.n_steps * args.envs
    print(f"{args.envs} robots on {args.workers} processes, {per_update:,} steps per PPO update, network on {device}")

    # --- the live window: a separate robot in THIS process, driven by the current policy ---
    demo = G1BackflipEnv(torque_scale=args.torque_scale)
    viewer = None
    if not args.no_viewer:
        import mujoco.viewer
        viewer = mujoco.viewer.launch_passive(demo.model, demo.data)
        viewer.cam.distance, viewer.cam.elevation, viewer.cam.azimuth = 3.2, -12, 90
        viewer.cam.lookat[:] = [0, 0, 0.8]

    def overlay(text_left, text_right):
        try:
            import mujoco
            viewer.set_texts((mujoco.mjtFontScale.mjFONTSCALE_150, mujoco.mjtGridPos.mjGRID_TOPLEFT,
                              text_left, text_right))
        except Exception:
            pass

    # The window runs in its own thread on a CPU copy of the policy, refreshed after
    # every update, so watching never slows training down.
    import copy
    import threading
    snap_lock = threading.Lock()
    snap = {"policy": copy.deepcopy(agent.policy).to("cpu"), "update": 0, "steps": 0,
            "mean": venv.obs_rms.mean.copy(), "var": venv.obs_rms.var.copy()}

    def refresh_snapshot(update, steps):
        state = {k: v.detach().cpu() for k, v in agent.policy.state_dict().items()}
        with snap_lock:
            snap["policy"].load_state_dict(state)
            snap["mean"], snap["var"] = venv.obs_rms.mean.copy(), venv.obs_rms.var.copy()
            snap["update"], snap["steps"] = update, steps

    def demo_loop():
        attempt = 0
        while viewer.is_running():
            attempt += 1
            obs, _ = demo.reset(seed=attempt)
            landed = False
            for _ in range(demo.max_steps):
                with snap_lock:
                    o = np.clip((obs - snap["mean"]) / np.sqrt(snap["var"] + 1e-8), -10, 10)
                    act, _ = snap["policy"].predict(o.astype(np.float32), deterministic=True)
                    update, steps = snap["update"], snap["steps"]
                obs, _, term, trunc, info = demo.step(act)
                landed = landed or info.get("landed", False)
                with viewer.lock():
                    viewer.cam.lookat[0] = demo.data.qpos[0]
                overlay("update\nsteps\nrotation\nheight\nlanded",
                        f"{update}\n{steps/1e6:.1f} M\n{np.degrees(demo.angle):.0f} deg\n"
                        f"{demo.data.qpos[2]:.2f} m\n{'YES' if landed else 'no'}")
                viewer.sync()
                time.sleep(demo.dt * args.slowmo)
                if term or trunc or not viewer.is_running():
                    break
            time.sleep(0.6)

    if viewer is not None:
        threading.Thread(target=demo_loop, daemon=True).start()

    class Live(BaseCallback):
        def __init__(self):
            super().__init__()
            self.update, self.t0, self.s0 = 0, time.time(), None
            self.ep_angle, self.ep_land, self.ep_touch, self.ep_stuck = [], [], [], []
            self.best_land = -1.0

        def _on_step(self):
            for done, info in zip(self.locals["dones"], self.locals["infos"]):
                if done:
                    self.ep_angle.append(np.degrees(info.get("angle", 0.0)))
                    self.ep_land.append(bool(info.get("landed", False)))
                    self.ep_touch.append(float(info.get("touch_up", np.nan)))
                    self.ep_stuck.append(bool(info.get("stuck", False)))
            return True

        def _on_rollout_end(self):
            self.update += 1
            if self.s0 is None:
                self.s0 = self.num_timesteps - per_update
            sps = (self.num_timesteps - self.s0) / max(time.time() - self.t0, 1e-6)
            buf = self.model.ep_info_buffer
            ret = np.mean([e["r"] for e in buf]) if buf else float("nan")
            ang = np.array(self.ep_angle[-400:]) if self.ep_angle else np.zeros(1)
            land = float(np.mean(self.ep_land[-400:])) if self.ep_land else 0.0
            stuck = float(np.mean(self.ep_stuck[-400:])) if self.ep_stuck else 0.0
            std = float(np.exp(self.model.policy.log_std.detach().cpu().numpy()).mean())
            print(f"upd {self.update:4d}  {self.num_timesteps/1e6:6.2f}M  {sps:6.0f} st/s  return {ret:7.1f}  "
                  f"rotation mean {ang.mean():4.0f} best {ang.max():4.0f} deg  "
                  f"upright@touchdown {np.nanmean(self.ep_touch[-400:]) if np.isfinite(self.ep_touch[-400:]).any() else float('nan'):+.2f}  "
                  f"landed {100*land:5.1f}%  stuck {100*stuck:5.1f}%  std {std:.2f}",
                  flush=True)
            if self.update % 20 == 0:
                self._save("latest")
                score = stuck + 0.01 * land       # stuck landings first, touchdowns break ties
                if score > self.best_land and len(self.ep_land) >= 200:
                    self.best_land = score
                    self._save("best")
            if viewer is not None:
                refresh_snapshot(self.update, self.num_timesteps)

        def _save(self, name):
            d = runs / name
            d.mkdir(exist_ok=True)
            self.model.save(str(d / "model.zip"))
            venv.save(str(d / "vecnorm.pkl"))

    cb = Live()
    try:
        agent.learn(total_timesteps=int(args.steps), callback=cb, reset_num_timesteps=not args.resume)
    except KeyboardInterrupt:
        print("stopped by you")
    cb._save("latest")
    print(f"saved to {runs / 'latest'}")
    venv.close()
    if viewer is not None:
        viewer.close()


if __name__ == "__main__":
    main()
