import numpy as np, pickle, mujoco
from stable_baselines3 import PPO
from backflip_env import G1BackflipEnv
env = G1BackflipEnv(); m, d = env.model, env.data
agent = PPO.load("runs/latest/model.zip", device="cpu")
vn = pickle.load(open("runs/latest/vecnorm.pkl", "rb"))
for ep in range(6):
    obs, _ = env.reset(seed=200 + ep); t_land = None; trace = []
    for k in range(env.max_steps):
        o = np.clip((obs - vn.obs_rms.mean) / np.sqrt(vn.obs_rms.var + 1e-8), -10, 10)
        a, _ = agent.predict(o.astype(np.float32), deterministic=True)
        obs, r, term, trunc, info = env.step(a)
        t = (k + 1) * env.dt
        if env.landed and t_land is None: t_land = t
        if t_land is not None and len(trace) < 40 and k % 3 == 0:
            trace.append(f"{d.qpos[2]:.2f}/{env._up():+.1f}/{d.qvel[0]:+.1f}")
        if term or trunc: break
    bodies = sorted({m.body(m.geom_bodyid[c.geom2 if c.geom1 == env.floor else c.geom1]).name
                     for c in d.contact[:d.ncon] if env.floor in (c.geom1, c.geom2)})
    print(f"ep{ep}: landed at {t_land}, ended {t:.2f}s term={term} touching={bodies}")
    print("   after landing, every 3rd step  z/up/vx:", " ".join(trace[:14]))
