"""A backflip as a Gymnasium environment for the Unitree G1.

Built on the course package (`soc4180`) but deliberately different from the
week 7 walker, because a flip is a different problem:

- **Realistic torque limits.** The Menagerie G1 ships with *no* force limits,
  i.e. infinitely strong motors. A flip under that model proves nothing, so
  every actuator is capped at the real G1's rated torque (Unitree URDF values).
- **Privileged observation.** Simulation only, so the policy may see body
  height, world velocity and how far it has rotated. A real robot would need a
  state estimator for these (week 6); here it would only slow learning down.
- **23 controlled joints.** Legs, waist and arms. Arms matter: swinging them
  is how a gymnast adds angular momentum. Wrists are held.
- **A timed reference, not a motion capture.** The reward asks for one number,
  the flip angle, to follow a schedule: crouch, rotate 360 degrees backwards,
  land. How the body achieves that is left to PPO.
- **Anything but the feet touching the floor ends the episode.** That is what
  makes "fall over backwards" (which also rotates!) a dead end instead of a
  cheap partial solution.
"""

from __future__ import annotations

import numpy as np

import mujoco
import gymnasium as gym
from gymnasium import spaces

import soc4180
from soc4180.walking import WalkingController

TWO_PI = 2.0 * np.pi

# Rated torques (N*m) from Unitree's G1 URDF. Matched by substring, first hit wins.
TORQUE_LIMITS = [
    ("hip_roll", 139.0), ("hip", 88.0), ("knee", 139.0), ("ankle", 50.0),
    ("waist_yaw", 88.0), ("waist", 50.0),
    ("shoulder", 25.0), ("elbow", 25.0), ("wrist_roll", 25.0), ("wrist", 5.0),
]

# Controlled joints and how far (rad) a full +/-1 action moves each from nominal.
CONTROLLED = [
    ("hip_pitch", 1.5), ("hip_roll", 0.4), ("hip_yaw", 0.3), ("knee", 1.4),
    ("ankle_pitch", 0.7), ("ankle_roll", 0.25),
    ("waist_yaw", 0.3), ("waist_roll", 0.3), ("waist_pitch", 0.5),
    ("shoulder_pitch", 2.0), ("shoulder_roll", 0.8), ("shoulder_yaw", 0.5), ("elbow", 1.2),
]

# Hand-made reference poses, one per phase of a gymnast's backflip (radians).
# G1 signs: hip pitch < 0 bends the thigh forward, knee > 0 bends, ankle pitch > 0
# points the toes, shoulder pitch < 0 raises the arm forward/up.
# (time s, hip_pitch, knee, ankle_pitch, shoulder_pitch, elbow), both sides equal.
KEYFRAMES = [
    (0.00, -0.35, 0.70, -0.35,  0.20, 0.30),   # start: the course's walking crouch
    (0.35, -0.90, 1.60, -0.70,  0.80, 0.30),   # load: deep crouch, arms swung back
    (0.55, -0.10, 0.10,  0.40, -2.80, 0.00),   # launch: legs extend, arms whip overhead
    (0.80, -2.00, 2.20, -0.30, -1.20, 1.00),   # tuck: knees to chest, hands to shins
    (0.95, -2.00, 2.20, -0.30, -1.20, 1.00),   # hold the tuck through the spin
    (1.20, -0.80, 1.30, -0.50, -1.20, 0.30),   # open: legs under the body, arms forward
    (1.50, -0.35, 0.70, -0.35,  0.20, 0.30),   # land: back to the crouch
]
POSE_JOINTS = ["hip_pitch", "knee", "ankle_pitch", "shoulder_pitch", "elbow"]


def reference_pose(t: float) -> np.ndarray:
    """The five keyframe joint angles at time t, smoothly interpolated."""
    times = [k[0] for k in KEYFRAMES]
    if t >= times[-1]:
        return np.array(KEYFRAMES[-1][1:])
    i = int(np.searchsorted(times, t, side="right")) - 1
    (t0, *a), (t1, *b) = KEYFRAMES[i], KEYFRAMES[i + 1]
    s = (t - t0) / (t1 - t0)
    s = s * s * (3.0 - 2.0 * s)
    return (1 - s) * np.array(a) + s * np.array(b)


REWARD = {
    "flip": 3.0,      # follow the flip-angle schedule -- the actual goal
    "pose": 2.0,      # match the keyframe body pose of the current phase
    "height": 4.0,    # get airborne while the flip is supposed to be happening
    "upright": 1.0,   # after the schedule ends: be upright ...
    "stand": 1.0,     # ... at standing height
    "land": 20.0,     # one-off bonus: 360 degrees done, feet down, upright
    "stick": 3.0,     # every step after landing that it is still standing
    "stuck": 60.0,    # one-off, at the end: landed AND still standing -- the real goal
    "touchdown": 30.0,  # one-off, at the first foot contact after the spin: more for closer to 360
    "still": 1.5,     # after the flip: little horizontal speed, so the landing can be held
    "smooth": -0.02,  # penalise jerky action changes
}


def flip_schedule(t: float, t0: float, duration: float) -> float:
    """Reference flip angle (rad) at time t: 0, then a smooth 0 -> 2*pi, then 2*pi."""
    s = np.clip((t - t0) / duration, 0.0, 1.0)
    return TWO_PI * s * s * (3.0 - 2.0 * s)      # smoothstep


class G1BackflipEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(
        self,
        *,
        control_hz: float = 50.0,
        episode_seconds: float = 3.2,
        flip_start: float = 0.45,
        flip_duration: float = 0.75,
        torque_scale: float = 1.0,
        reward_weights: dict | None = None,
    ):
        self.model = soc4180.load_g1()
        self.data = mujoco.MjData(self.model)
        m = self.model

        # -- realistic motors -------------------------------------------------------
        self.torque = np.zeros(m.nu)
        for a in range(m.nu):
            name = m.actuator(a).name
            self.torque[a] = next(v for k, v in TORQUE_LIMITS if k in name) * torque_scale
        m.actuator_forcelimited[:] = 1
        m.actuator_forcerange[:, 0] = -self.torque
        m.actuator_forcerange[:, 1] = self.torque

        # -- nominal pose: the course's walking crouch --------------------------------
        self.nominal = WalkingController(m).nominal.copy()
        self.nominal[2] = 0.755
        self.act_qpos = np.array([m.jnt_qposadr[m.actuator_trnid[a, 0]] for a in range(m.nu)])
        self.act_dof = np.array([m.jnt_dofadr[m.actuator_trnid[a, 0]] for a in range(m.nu)])

        ctrl_act, scale = [], []
        for a in range(m.nu):
            name = m.actuator(a).name
            hit = next((s for k, s in CONTROLLED if k in name), None)
            if hit is not None:
                ctrl_act.append(a)
                scale.append(hit)
        self.ctrl_act = np.array(ctrl_act)          # actuator indices the policy drives
        self.scale = np.array(scale)
        jr = m.jnt_range[m.actuator_trnid[self.ctrl_act, 0]]
        self.lo, self.hi = jr[:, 0], jr[:, 1]

        # -- contact bookkeeping: only the feet may touch the floor ------------------------
        # -- the ten joints the keyframes describe: (left, right) x POSE_JOINTS ---------
        self.pose_qpos = np.array([
            m.jnt_qposadr[mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_JOINT, f"{side}_{j}_joint")]
            for side in ("left", "right") for j in POSE_JOINTS])

        self.floor = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_GEOM, "floor")
        # both ankle links are "foot": landing on the heels touches the ankle_pitch link
        feet = {mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_BODY, f"{s}_ankle_{j}_link")
                for s in ("left", "right") for j in ("roll", "pitch")}
        self.foot_geom = np.array([m.geom_bodyid[g] in feet for g in range(m.ngeom)])
        self.pelvis = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_BODY, "pelvis")

        self.weights = dict(REWARD)
        if reward_weights:
            self.weights.update(reward_weights)
        self.decimation = max(int(round(1.0 / (control_hz * m.opt.timestep))), 1)
        self.dt = self.decimation * m.opt.timestep
        self.max_steps = int(round(episode_seconds / self.dt))
        self.t0, self.T = flip_start, flip_duration
        self.t_end = flip_start + flip_duration

        n = len(self.ctrl_act)
        self.action_space = spaces.Box(-1.0, 1.0, (n,), dtype=np.float32)
        self.observation_space = spaces.Box(-np.inf, np.inf, (14 + 10 + 3 * n,), dtype=np.float32)
        self._prev = np.zeros(n, dtype=np.float32)

    # ------------------------------------------------------------------ gym API
    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        mujoco.mj_resetData(self.model, self.data)
        self.data.qpos[:] = self.nominal
        q = self.act_qpos[self.ctrl_act]
        self.data.qpos[q] += self.np_random.uniform(-0.03, 0.03, len(q))
        mujoco.mj_forward(self.model, self.data)
        self._prev[:] = 0.0
        self.step_count = 0
        self.angle = 0.0            # accumulated backward rotation (rad)
        self.max_height = float(self.data.qpos[2])
        self.landed = False
        self.touched = False
        self.touch_up = np.nan      # pelvis uprightness at touchdown (1 = perfectly upright)
        return self._obs(), {}

    def step(self, action):
        a = np.clip(np.asarray(action, dtype=np.float32), -1.0, 1.0)
        target = self.nominal[self.act_qpos].copy()
        target[self.ctrl_act] = np.clip(target[self.ctrl_act] + self.scale * a, self.lo, self.hi)

        m, d = self.model, self.data
        bad_contact = False
        for _ in range(self.decimation):
            d.ctrl[:] = target
            mujoco.mj_step(m, d)
            # backward rotation = negative spin about the world y axis (robot faces +x)
            w_world = d.xmat[self.pelvis].reshape(3, 3) @ d.qvel[3:6]
            self.angle += -w_world[1] * m.opt.timestep
            bad_contact = bad_contact or self._bad_contact()
        self.step_count += 1
        self.max_height = max(self.max_height, float(d.qpos[2]))

        reward, info = self._reward(a)
        # First foot contact after most of a turn (it must have been airborne): pay for
        # the pelvis REALLY being upright, not for the counted angle -- the counted angle
        # only sees rotation about world y, and a twisting diagonal spin fooled it.
        if not self.touched and self.angle > 4.7 and self._feet_down():
            self.touched = True
            self.touch_up = self._up()
            # ... and for NOT flying backwards: landings at -2.6 m/s all buckled
            vx = float(self.data.qvel[0])
            reward += self.weights["touchdown"] * max(0.0, self.touch_up) ** 2 * np.exp(-vx * vx / 1.0)
        done_flip = self.angle > TWO_PI - 0.5
        terminated = False
        if bad_contact or self.angle < -1.0 or self.angle > TWO_PI + 1.2:
            terminated = True
            if bad_contact:
                reward -= 5.0
        elif done_flip and not self.landed and self._feet_down() and self._up() > 0.7:
            self.landed = True
            reward += self.weights["land"]
            info["landed"] = True
        # After landing, the reward is in STAYING up: a landing bonus paid at the instant
        # of touchdown taught "land, then collapse" (24 of 30 landed, 0 still standing).
        standing = self._up() > 0.8 and float(self.data.qpos[2]) > 0.55
        if self.landed and not terminated:
            reward += self.weights["stick"] * float(standing)
        truncated = self.step_count >= self.max_steps
        stuck = bool(truncated and not terminated and self.landed and standing)
        if stuck:
            reward += self.weights["stuck"]
        info.update(angle=self.angle, landed=self.landed, max_height=self.max_height,
                    touch_up=self.touch_up, stuck=stuck)
        self._prev[:] = a
        return self._obs(), reward, terminated, truncated, info

    # ------------------------------------------------------------------ internals
    def _time(self) -> float:
        return self.step_count * self.dt

    def _up(self) -> float:
        """How upright the pelvis is: its z axis dotted with world up (1 = upright)."""
        return float(self.data.xmat[self.pelvis][8])

    def _bad_contact(self) -> bool:
        d = self.data
        for i in range(d.ncon):
            c = d.contact[i]
            if c.geom1 == self.floor and not self.foot_geom[c.geom2]:
                return True
            if c.geom2 == self.floor and not self.foot_geom[c.geom1]:
                return True
        return False

    def _feet_down(self) -> bool:
        d = self.data
        for i in range(d.ncon):
            c = d.contact[i]
            if self.floor in (c.geom1, c.geom2):
                return True
        return False

    def _obs(self) -> np.ndarray:
        d = self.data
        t = self._time()
        R = d.xmat[self.pelvis].reshape(3, 3)
        q = d.qpos[self.act_qpos[self.ctrl_act]] - self.nominal[self.act_qpos[self.ctrl_act]]
        v = d.qvel[self.act_dof[self.ctrl_act]]
        return np.concatenate([
            [t / 2.6, flip_schedule(t, self.t0, self.T) / TWO_PI, self.angle / TWO_PI,
             d.qpos[2]],                              # clock, reference, progress, height
            R.T @ np.array([0.0, 0.0, -1.0]),          # gravity in the body frame (3)
            d.qvel[0:3],                               # world linear velocity (3)
            d.qvel[3:6] * 0.25,                        # body angular velocity (3)
            [float(self._feet_down())],
            np.tile(reference_pose(t), 2) - d.qpos[self.pose_qpos],   # how far from the keyframe (10)
            q, v * 0.05, self._prev,
        ]).astype(np.float32)

    def _reward(self, a):
        t = self._time()
        w = self.weights
        ref = flip_schedule(t, self.t0, self.T)
        z = float(self.data.qpos[2])
        pose = np.exp(-np.mean(np.square(np.tile(reference_pose(t), 2)
                                         - self.data.qpos[self.pose_qpos])) / 0.25)
        if t > self.t_end + 0.1 and self.angle < 5.0:
            pose = 0.0     # the landing crouch only counts after a real flip
        # Full 3-D orientation error against a PURE backflip (rotation about y only), so a
        # sideways twist scores badly even when the counted angle looks right.
        c, s = np.cos(-ref), np.sin(-ref)
        R_ref = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
        R = self.data.xmat[self.pelvis].reshape(3, 3)
        cos_err = np.clip((np.trace(R_ref.T @ R) - 1.0) / 2.0, -1.0, 1.0)
        orient = np.exp(-np.arccos(cos_err) ** 2 / 0.5)
        terms = {
            "flip": np.exp(-((self.angle - ref) ** 2) / 0.6) * orient,
            "pose": pose,
            # capped: past 0.5 m of extra height, jumping higher earns nothing
            "height": min(max(0.0, z - 0.72), 0.5) if self.t0 < t < self.t_end + 0.1 else 0.0,
            # only after a real rotation: standing still all episode must earn nothing here
            "upright": max(0.0, self._up()) if t > self.t_end + 0.1 and self.angle > 5.0 else 0.0,
            "stand": np.exp(-((z - 0.72) ** 2) / 0.01) if t > self.t_end + 0.1 and self.angle > 5.0 else 0.0,
            "still": float(np.exp(-float(np.sum(self.data.qvel[0:2] ** 2)) / 0.3))
                     if t > self.t_end and self.angle > 5.0 else 0.0,
            "smooth": float(np.mean(np.square(a - self._prev))),
        }
        reward = float(sum(w[k] * v for k, v in terms.items()))
        return reward, dict(terms)
