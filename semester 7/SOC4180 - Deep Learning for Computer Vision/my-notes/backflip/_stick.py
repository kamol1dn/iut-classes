import numpy as np, pickle
from stable_baselines3 import PPO
from backflip_env import G1BackflipEnv
env = G1BackflipEnv()
agent = PPO.load("runs/latest/model.zip", device="cpu")
vn = pickle.load(open("runs/latest/vecnorm.pkl", "rb"))
N = 30; landed = stuck = 0
for ep in range(N):
    obs, _ = env.reset(seed=100 + ep)
    for k in range(env.max_steps):
        o = np.clip((obs - vn.obs_rms.mean) / np.sqrt(vn.obs_rms.var + 1e-8), -10, 10)
        a, _ = agent.predict(o.astype(np.float32), deterministic=True)
        obs, r, term, trunc, info = env.step(a)
        if term or trunc: break
    landed += env.landed
    ok = env.landed and not term
    stuck += ok
    if ep < 8:
        print(f"ep{ep}: landed={env.landed} survived_to_end={not term} touch_up={env.touch_up:+.2f} "
              f"final z={env.data.qpos[2]:.2f} up={env._up():+.2f} maxz={env.max_height:.2f}")
print(f"deterministic policy, {N} attempts: landed {landed}, landed AND still standing at 2.6 s: {stuck}")
