# Lab 14: Drone Missions, prep sheet (2026-11-20)

Lab sheet: [`Lab.md`](../labs/soc3050code/projects2026_arm/14_Drone_Missions/Lab.md) ·
Deck: [`_slides/14_Drone_Missions.html`](../labs/soc3050code/projects2026_arm/_slides/14_Drone_Missions.html).
The lab isn't marked or collected. It has three contests: hold in a gale (Part 3), figure-8 (Part 5), and the race (Part 7).

## Already done

- Pulled `soc3050code` with 4 new upstream commits. This is the version that **runs in Wokwi**: lock-step `world`/`ctl` and the kernel fixes. Your 12_Game and 13 edits weren't touched.
- **Ran it as-is.** The host test passed 27 of 27 checks. Default mission: 57.7 s in still air, **61.0 s** in 8 m/s wind with 2.07 m max cross-track. Both are legal and match the sheet.
- **Trajectory changed (Part 5):** `mission.py --gen figure8`, plus a built-in figure-8 on the board.
- **New feature: an ORBIT flight mode.** The drone circles the HOLD point. The host test now passes **43 checks, 0 failed**. The 27 original checks print exactly the same output as before, so the feature does nothing unless you use it.
- Firmware: **0 warnings, FLASH 32 400 B (98.9 %), RAM 10 920 B**. The lesson was 30 092 B before, so ORBIT plus the figure-8 cost 2 308 B. Only **368 B of flash is free**, so keep any extra `say()` text short.
- `control_step`'s stack frame is **96 B before and after** (measured with `-fstack-usage`), so the `ctl` task's 224 words are not under extra pressure. `orbit()` is inlined into it.
- Nothing is committed. `origin` is the professor's repo.

### Running the host test on this laptop

gcc isn't on PATH. It lives at `D:\tools\winlibs-gcc15.2\mingw64\bin`. From the lesson's `host` folder:

```
$env:PATH="D:\tools\winlibs-gcc15.2\mingw64\bin;$env:PATH"; .\run.bat
```

## Change 1: the figure-8 (Lab Part 5)

`uv run mission.py --gen figure8 R ALT N` prints a lemniscate, `x = R sin t, y = R sin t cos t`, as N + 1 waypoints through home. It refuses N > 15 (the drone holds 16) and R > 50 m.

```
uv run mission.py --gen figure8 25 8 12 > my8.mission     (already made, in host\)
uv run mission.py my8.mission > my8.txt                    (already made)
out\sitl --fly 8 my8.txt
uv run mission.py --score out\fly.log --race
```

**Result in 8 m/s:** **70.4 s, legal**. Max cross-track was 2.21 m, RMS 0.86 m, worst waypoint 1.31 m, and it landed 0.55 m from home.

**The Part 5 question: where is cross-track worst?** At the **ends of the two loops** (wp 2→3→4 and 8→9, up to 1.88 m), where the legs turn about 73°. The **turn** at the crossing is 0°: legs 5→6 and 6→7 lie on one straight line through home. So the sheet's hint ("up to ~60° near the crossing") doesn't hold for N = 12. The crossing leg 6→7 still reached 1.74 m, from a gust partway along the leg, not a turn. That's one seed, so the two are close. The "max 2.21 m" is an artefact: wp 0 *is* home, so leg 0 has zero length and its "cross-track" is just takeoff drift.

**On the board:** type `fig8` on the ground, then press **A**. It loads the same 13 points (checked: identical to `my8.mission` to 0.1 m).
**Careful:** after `fig8`, button A keeps flying the figure-8 until you reset or send `$MISSION,CLEAR*39`. Lab Parts 2 and 7 assume the default mission.

## Change 2: ORBIT mode (the new feature)

Circle a point at radius `ORB_R`, nose along the track, for `ORB_LAPS` laps, then HOLD. Real autopilots have the same mode: PX4 Orbit, ArduPilot Circle.

| | |
|---|---|
| start | the shell word `orbit`, or the frame `$MODE,ORBIT*6D`, in **HOLD** (circles the hold point; steer it with the joystick first) or **MISSION** (circles where it is, pausing the mission; **A** resumes) |
| refused | on the ground or during takeoff → `STATE`; circle not inside the fence with 2 m to spare → `FENCE` |
| params | `ORB_R` 3-45 m (10), `ORB_LAPS` 0-20 (3, 0 = until B/SEL), `ORB_CW` 0/1 (0 = anticlockwise), `ORB_PRIO` 0/1 (1) |
| screen | OLED: dotted orbit circle + centre cross, panel `LAP 1/3`, a chirp each lap. Station: pink dashed circle, `LAP n/N`, `orbit` / `lap` in the event log |
| telemetry | `$EVT,t,ORBIT,cx_dm,cy_dm,r_dm,laps` on entry, `$EVT,t,LAP,n,laps` each lap |
| failsafes | fence and battery RTL still fire inside ORBIT (tested). The test allows 2.0 m for the landing, not 1.5 m, because RTL's own spread in 4 m/s is that wide. Over 11 seeds, HOLD-then-battery landed 0.28-1.77 m from home (mean 0.66) and ORBIT-then-battery 0.24-1.74 m (mean 0.77) |

**How it flies** (`flight.c`, `orbit()`):
- Like `leg()`, it splits the velocity into **along** the circle (cruise speed) and **across** it (KP_POS × radius error).
- Speed is capped so the turn needs no more than 40 % of the tilt: `v ≤ √(0.4·g·tan25°·r)`.
- It **spirals out** from the centre: tangential speed grows with d/r.
- **Feed-forward:** the centripetal `v²/r` is added before any error appears.
- **Radial priority (`ORB_PRIO=1`):** when a gust uses up the tilt, it keeps the inward pull and gives up speed. Plain scaling gives up both equally.

**Measured on the host:**

| case | radius error RMS / max (true) | lap |
|---|---|---|
| r 10 m, still air | 0.64 / 1.37 m | 17.7 s (ideal 15.7) |
| r 12 m, 5 m/s, 2 laps | 0.61 / 1.44 m | 20.7 s (ideal 18.8) |
| r 12 m, 8 m/s, 7 gust seeds, `ORB_PRIO=1` | mean **1.07 / 4.15 m** | mean 23.8 s |
| same, `ORB_PRIO=0` | mean 1.34 / 5.01 m | mean 22.6 s |

Radial priority is better on 4 of the 7 seeds (a lot on two) and slightly worse on 3. It costs about **5 % in lap time**. Lap time is measured from the angle swept, not by counting whole laps. The 4-12 m worst cases are **15 m/s gusts**: drag 0.35 × 15 > g tan 25°, so no mode can hold position. It's physics, not a bug.

```
out\sitl --orbit 8 ORB_R=15 ORB_CW=1 ORB_LAPS=2      (try your own; SEED=12 to change the gusts)
```

## Wokwi steps

1. `build.bat` (or use the `Main.elf` already built). Then open https://wokwi.com/projects/new/st-nucleo-c031c6, paste `diagram.json`, upload `Main.elf`.
2. The banner's shell line should end `fig8  orbit`.
3. **ORBIT:** wait 1 s, press **a**, and **wait until the OLED says MISSION** (`orbit` is refused during TAKEOFF, and SEL during the climb holds at a half-way altitude). Press **SEL** (HOLD), nudge the joystick, then type `orbit`. Watch the circle and `LAP n/3`. When it's done it HOLDs, and **a** resumes the mission. (Typing `orbit` straight from MISSION also works: it circles where it is.)
4. **Figure-8:** reset, type `fig8`, press **a**. Copy the serial monitor into `capture.txt`, then run `uv run host\mission.py --score capture.txt --race`.
5. Frames to paste: `$PARAM,ORB_R,15*19`, `$PARAM,ORB_LAPS,0*71`, `$PARAM,ORB_CW,1*6A`, `$PARAM,ORB_PRIO,0*7B`, `$PARAM,WIND,80*53` (8 m/s; the knob gives it back), `$MODE,ORBIT*6D`.
6. Station: type `orbit` / `fig8` in its command line. There's no key for them, because a new key would mean changing the shared `_lib/kbd.c`.

## Where it is in the code

| What | Where |
|---|---|
| ORBIT control law, laps | `flight.c:451` `orbit()` |
| entry checks (state, fence) | `flight.c:205` in `fc_set_mode()` |
| feed-forward + radial priority | `flight.c:596-611` in `control_step()` |
| failsafes include ORBIT | `flight.c:376` |
| the params `ORB_*` | `flight.c:76` |
| built-in figure-8 | `flight.c:290` `fc_mission_figure8()` |
| `$MODE,ORBIT`, `$EVT ORBIT/LAP` | `mavlite.c:67`, `mavlite.c:192` |
| OLED circle + `LAP` | `ui.c:63`, `ui.c:100` |
| shell words | `Main.c:301` `cmd_fig8`, `Main.c:311` `cmd_orbit` |
| `--gen figure8` | `host/mission.py:132` |
| host tests, `--orbit` | `host/sitl.c:280`, section 10 at `:511` |
| station view | `tools/station/views/l14_mission.py` |

## Your log: the "not watched in Wokwi" items (fill in during class)

| Item | Host / predicted | Wokwi says |
|---|---|---|
| Part 2: default mission, knob 500 | 57.7 s | |
| Part 5: fig8 score, knob 800 | 70.4 s, legal | |
| ORBIT: OLED circle drawn where the drone flies? | yes (`out\oled_orbit.txt`) | |
| ORBIT: lap time, r 10 m | ~17.7 s | |
| ORBIT 8 m/s: drone pushed out on the downwind side? | yes, in gusts | |
| `stats`: ctl max µs with ORBIT on vs off | (new: more float maths) | |
| `stats`: ctl stack N of 224 words, after an orbit | frame unchanged (96 B) | |
| `stats`: world overruns | 0 on silicon | |
