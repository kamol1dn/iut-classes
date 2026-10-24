"""SubprocVecEnv, but each worker process steps SEVERAL robots per message.

SB3's SubprocVecEnv sends one message per robot per step. On Windows that pipe
round trip costs more than the physics, so 15 processes delivered ~3k steps/s
against ~11.6k measured raw. Batching k robots per worker amortises it k-fold.
"""

from __future__ import annotations

import multiprocessing as mp

import numpy as np
from stable_baselines3.common.vec_env.base_vec_env import VecEnv


def _worker(remote, fns):
    envs = [f() for f in fns]
    try:
        while True:
            cmd, arg = remote.recv()
            if cmd == "step":
                out = []
                for env, a in zip(envs, arg):
                    obs, r, term, trunc, info = env.step(a)
                    done = term or trunc
                    if done:
                        info["terminal_observation"] = obs
                        info["TimeLimit.truncated"] = trunc and not term
                        obs, _ = env.reset()
                    out.append((obs, r, done, info))
                remote.send(out)
            elif cmd == "reset":
                remote.send([env.reset()[0] for env in envs])
            elif cmd == "spaces":
                remote.send((envs[0].observation_space, envs[0].action_space))
            elif cmd == "close":
                break
    except (KeyboardInterrupt, EOFError, BrokenPipeError):
        pass
    finally:
        remote.close()


class BatchedSubprocVecEnv(VecEnv):
    def __init__(self, env_fns, n_workers: int):
        chunks = [list(c) for c in np.array_split(np.array(env_fns, dtype=object), n_workers) if len(c)]
        self.sizes = [len(c) for c in chunks]
        ctx = mp.get_context("spawn")
        self.remotes, self.procs = [], []
        for c in chunks:
            parent, child = ctx.Pipe()
            p = ctx.Process(target=_worker, args=(child, c), daemon=True)
            p.start()
            child.close()
            self.remotes.append(parent)
            self.procs.append(p)
        self.remotes[0].send(("spaces", None))
        obs_space, act_space = self.remotes[0].recv()
        super().__init__(len(env_fns), obs_space, act_space)
        self._actions = None

    def reset(self):
        for r in self.remotes:
            r.send(("reset", None))
        obs = [o for r in self.remotes for o in r.recv()]
        self.reset_infos = [{} for _ in range(self.num_envs)]
        return np.stack(obs)

    def step_async(self, actions):
        i = 0
        for r, n in zip(self.remotes, self.sizes):
            r.send(("step", actions[i:i + n]))
            i += n

    def step_wait(self):
        res = [x for r in self.remotes for x in r.recv()]
        obs, rew, done, info = zip(*res)
        return np.stack(obs), np.array(rew, dtype=np.float32), np.array(done), list(info)

    def close(self):
        for r in self.remotes:
            try:
                r.send(("close", None))
            except Exception:
                pass
        for p in self.procs:
            p.join(timeout=2)

    # --- parts of the VecEnv interface this project never uses ----------------------
    def get_attr(self, attr_name, indices=None):
        return [None] * self.num_envs

    def set_attr(self, attr_name, value, indices=None):
        pass

    def env_method(self, method_name, *args, indices=None, **kwargs):
        return [None] * self.num_envs

    def env_is_wrapped(self, wrapper_class, indices=None):
        return [False] * self.num_envs
