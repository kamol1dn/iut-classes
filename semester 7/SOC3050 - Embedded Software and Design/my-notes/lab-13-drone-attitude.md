# Lab 13: Drone Attitude, prep sheet (2026-11-13)

Lab sheet: [`Lab.md`](../labs/soc3050code/projects2026_arm/13_Drone_Attitude/Lab.md) ·
Deck: [`_slides/13_Drone_Attitude.html`](../labs/soc3050code/projects2026_arm/_slides/13_Drone_Attitude.html).
The lab isn't marked or collected. Part 1 has a scoreboard, and Part 8 is open-ended.

## Already done

- Pulled `soc3050code` (6 new commits on lesson 13; your 12_Game WAVE edits weren't touched).
- `build.bat` gives **0 warnings, FLASH 28 768 B / RAM 11 144 B**, the same as the sheet. `Main.elf` is ready.
- Host test gives **PASSED: 0 of 24 checks failed**.
- `host\sitl.exe score 9 0.12` gives 0.620 and `score 12 0.12` gives 0.454, both the same as the sheet.

### Gotcha: `host\run.bat` on this laptop

- gcc isn't on PATH. It lives at `D:\tools\winlibs-gcc15.2\mingw64\bin`.
- `NoDefaultCurrentDirectoryInExePath=1` is set, so the bare `sitl.exe` line inside `run.bat` fails.
- `sitl.exe` is already built, so just run it with a path:

```
host\sitl.exe                 :: the full 24-check test
host\sitl.exe score 9 0.12    :: the contest
```

To rebuild it after you change `control.c` (PowerShell, from the lesson folder):

```
$env:PATH="D:\tools\winlibs-gcc15.2\mingw64\bin;$env:PATH"; cd host; gcc -std=c11 -O2 -Wall -Wextra -I.. -I..\..\_lib -o sitl.exe sitl.c ..\world.c ..\control.c -lm; cd ..
```

## Wokwi setup (Part 0)

1. Open https://wokwi.com/projects/new/st-nucleo-c031c6 and paste `diagram.json` (it adds the MPU6050).
2. Upload `Main.elf` and start the sim.
3. Check the banner and the OLED. It should say **250Hz**. If it shows less, write the number down.
4. Keys: **A** arm, **B** gust, **SEL** SIM/MPU, **knob** Kp ×0.125–×8.
5. Shell commands: `stats alpha aw mix kick hold quiet loud`. A restart resets everything.

## Where each part points in the code

| Part | What to look at | Where |
|---|---|---|
| 1 contest | the five gains (`alpha 0.98, angle_kp 9, rate_kp 0.12, rate_ki 0.15, rate_kd 0.0008`) | `control.c:52-65` (`control_init`) |
| 2/3 alpha | complementary filter (gyro integrate + accel blend) | `control.c:~140-160` |
| 4 "find the `if`" | anti-windup: integrate freely vs clamp to `i_limit` | `control.c:107-112` (`rate_pid`) |
| 4 note | yaw has its own anti-windup: `if (!s.saturated)` | `control.c:197` |
| 7 signs | MPU axis mapping: Y and Z negated | `Main.c:251-264` (`mpu_sense`) |

## Host numbers to compare against (from `sitl.exe` just now)

| alpha | est err RMS | est err max | note |
|---|---|---|---|
| 0 | 3.18° | 7.18° | accel only: jitter |
| 0.9 | 0.33° | 1.32° | |
| **0.98** | **0.20°** | 0.57° | best, the default |
| 0.995 | 0.60° | 0.79° | |
| 1.0 | 14.54° | 26.15° | gyro only: drifts, failsafe blind |

- **Gust:** 11.2° peak, back inside 3° in 0.166 s.
- **Anti-windup:** on, it peaks at 29.8°. Off, it goes to 179.5° and trips the TILT failsafe.
- **`mix -1`:** TILT 0.36 s later, then a crash.

## Your log: the "not watched in Wokwi" items (fill in during class)

| Item | Host / predicted | Wokwi says |
|---|---|---|
| Loop rate on OLED | 250 Hz | |
| SIM estimate vs truth (dotted vs solid) | 0.20° RMS | |
| Part 1: my best gains / score | beat 0.278 | |
| Part 1: does it feel better in Wokwi? | | |
| Part 5 `stats`: world_step+sense cycles | ~33 900 | |
| Part 5 `stats`: control_step cycles | ~26 000 | |
| Part 5 bad checksums in `host.py` | 0 | |
| Part 7: `accelY` +0.5 g → roll sign | **+26.6°** (Y left) | |
| Part 7: `rotationX` 5 °/s → settled error | 0.98° | |
| Part 7: same with `alpha 1000` | ramps 5°/s | |
| Part 7: does Wokwi honour DLPF? late wake-ups? | open question | |
