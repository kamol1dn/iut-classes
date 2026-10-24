import numpy as np, mujoco, pickle
from stable_baselines3 import PPO
from backflip_env import G1BackflipEnv
env = G1BackflipEnv()
agent = PPO.load("runs/latest/model.zip", device="cpu")
vn = pickle.load(open("runs/latest/vecnorm.pkl", "rb"))
m, d = env.model, env.data
for ep in range(6):
    obs, _ = env.reset(seed=ep)
    first_contact = None
    for k in range(env.max_steps):
        o = np.clip((obs - vn.obs_rms.mean) / np.sqrt(vn.obs_rms.var + 1e-8), -10, 10)
        a, _ = agent.predict(o.astype(np.float32), deterministic=True)
        obs, r, term, trunc, info = env.step(a)
        if env.angle > 3.5 and first_contact is None and env._feet_down():
            bodies = set()
            for i in range(d.ncon):
                c = d.contact[i]
                g = c.geom2 if c.geom1 == env.floor else c.geom1
                bodies.add(m.body(m.geom_bodyid[g]).name)
            first_contact = (round(k * env.dt, 2), round(np.degrees(env.angle)), round(env._up(), 2),
                             round(float(d.qpos[2]), 2), sorted(bodies))
        if term or trunc:
            break
    print(f"ep{ep}: ended t={k*env.dt:.2f}s term={term} angle={np.degrees(env.angle):.0f} up={env._up():.2f} "
          f"z={d.qpos[2]:.2f} maxz={env.max_height:.2f}\n   first ground touch after 200deg: {first_contact}")
