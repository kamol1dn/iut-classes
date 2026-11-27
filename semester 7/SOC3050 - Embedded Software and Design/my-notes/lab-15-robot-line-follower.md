# Lab 15: Robot Line Follower, prep sheet (2026-11-27)

Lab sheet: [`Lab.md`](../labs/soc3050code/projects2026_arm/15_Robot_Line_Follower/Lab.md) ·
Deck: [`_slides/15_Robot_Line_Follower.html`](../labs/soc3050code/projects2026_arm/_slides/15_Robot_Line_Follower.html).
The lab isn't marked or collected. Part 4 is a leaderboard (fastest clean lap), Part 8 is "your turn".

## Already done

- Pulled `soc3050code`: already up to date (lesson 15 has the Wokwi lock-step fix from 2026-11-16). Your 12/13/14 edits weren't touched.
- **Ran it as-is.** Host test: `PASS: 0 failure(s)`, and the numbers match the sheet (OVAL 5.12 s, S-BENDS 5.07, HAIRPINS 7.46, FIGURE-8 5.99 at knob 500). Firmware: 0 warnings, FLASH 29 968 B, RAM 9 832 B, same as the README.
- **New feature: a ghost car.** The OLED replays your best lap as a small hollow ring racing beside the robot, and after every lap prints how far ahead (`-`) or behind (`+`) of the ghost that lap was.
- Host test with the ghost: still `PASS`, a new table 10 with 3 checks. Tables 1-9 print exactly the same lines as before, so the controller and the race are unchanged.
- Firmware with the ghost: **0 warnings, FLASH 30 728 B (93.8 %), RAM 10 368 B (84.4 %)**. The ghost cost 760 B of flash and 536 B of RAM (two 128-sample paths). About 2 KB of flash is still free.
- Nothing is committed. `origin` is the professor's repo.
- **Nothing here was watched in Wokwi.** The ghost was run on the PC only.

### Running the host test on this laptop

gcc isn't on PATH. From the lesson folder:

```
$env:PATH="D:\tools\winlibs-gcc15.2\mingw64\bin;$env:PATH"; .\host\run.bat
```

## The ghost car

| | |
|---|---|
| what you see | a 5×5 hollow ring on the track, at the place the best lap was at the same lap time; the robot stays the solid triangle |
| lap gap | bottom right of the OLED after each lap: `-0.08` = this lap beat the ghost by 0.08 s, `+3.25` = lost by 3.25 s. Shown only while racing |
| which lap is the ghost | the fastest lap recorded so far on this track, auto or manual |
| survives | **A** (stop, back to the line) and a new start, so you can change the knob or gains and race the old lap |
| forgotten | when you change track (**B** or the menu) or reset the board |
| not kept | a lap longer than 12.8 s (128 samples at 10 Hz) |
| off / on | shell: `ghost 0`, `ghost 1` |

**Why you may not see it at first.** Inside one run at fixed settings every lap after the first is nearly identical, so the ring sits right on top of the triangle. It separates when something changes between the ghost's lap and this one:

- lap 2 of a run: the ghost is lap 1, which started from standstill, so the robot pulls ahead of it;
- after **A**, **A** with a different knob;
- after a shell change (`kd 0`, `slow 0`, `noise 80`...);
- in manual mode (**SEL**): Lab Part 1, "beat the robot", with the robot's lap on screen to chase.

**Measured on the host (table 10), OVAL:**

| run | knob | ghost lap after the run | last lap vs ghost |
|---|---|---|---|
| 1 | 400 | 6.34 s (lap 1 was 6.41) | -0.07 s |
| 2 | 500 | **5.12 s** (new ghost) | -0.085 s |
| 3 | 300 | 5.12 s (kept: slower run doesn't replace it) | +3.255 s |

**How it works** (`view.c`, `view_ghost()`): the display task calls it 10 times a second with a copy of the world. Slot `k = lap time / 100 ms` stores the robot's screen position. When the lap counter goes up, the lap's time is compared with the ghost's; a faster lap is copied over it. The ring is drawn with XOR like the robot, so erasing it restores the track underneath and only one or two OLED pages are resent.

It reads the world's true position, which the controller is not allowed to see. That's fine: the ghost is display code, on the same side of the wall as the OLED triangle. `control.c` is untouched, so every lab number still applies.

## Track 5: BANANA (Lab Part 8, "Design a track"; the professor's shape)

The professor asked for "a banana, but the lower half is a half circle". `track.c`: `{600,90} {120,170} {367,-160} {120,170} {600,90}`. It starts at the bottom of the half circle, heading east.

- **Lower edge:** an exact half circle, R 600 mm.
- **Upper edge:** curves the same way but flatter (R 367, 160°), so the middle (~320 mm) is thicker than the tips (240 mm).
- **Tips:** 170° U-turns on R 120.
- **Turns:** 90 + 170 - 160 + 170 + 90 = 360.
- **Closure:** tip end x = 600 - 120 - 120 sin 80 = 361.8, so R2 = 361.8 / sin 80 = 367.4. 367 leaves a 1 mm miss.
- **Host:** closure miss **1.00 mm** (limit 2), 72 points, 3617 mm, box 1199 × 720. Default knob: **3.96 s** a lap, max error 5.5 mm. Fastest knob that finishes: **675** (3.24 s), the same limit as HAIRPINS, set by the 120 mm tips.
- An earlier version of track 5 was a HEART (seen racing in Wokwi), but other students had done a heart. The BANANA firmware is built and passes on the host but **has not been watched in Wokwi yet**.
- The menu rows moved up 1 px each so that five tracks fit. The station draws the banana only after it is restarted.

## Bug fixed in the lesson: fake 0.00 s lap

`Main.c:311` used `if (w.laps != laps_seen)`. Changing track (or **A** back to the line) resets laps 1 → 0, which counted as a lap: `lap 0.00 s BEST` and `$LAP,2,0`. That frame would win the Part 4 leaderboard. Seen in Wokwi, fixed to `>`.

## Seen in Wokwi (2026-11-27, via the station)

- OVAL lap 1: **5.32 s** (host 5.20). S-BENDS lap 1: **5.26 s** (host 5.07). Within about 0.2 s, so the SITL chain holds on the chip.
- Heavy slow motion: about 0.3 s of race time per 15 s of real time at first. A lap takes minutes of wall clock.
- The joystick menu direction is right (Up wraps from 1 to 5).

## Gotchas for the lab parts

- **Part 2:** estimate (field 2) and true error (field 3) have **opposite signs**. Flip one before comparing.
- **Part 3:** `kd 0` is fine at knob 500 and weaves at 700 (12.56 s vs 3.80 s). Put `kd 1` back.
- **Part 4 targets:** S-BENDS knob 775 → 3.72 s, HAIRPINS knob 675 → 6.03 s. `slow 0` makes HAIRPINS worse by 0.65 s. Use the ghost: set a lap, press **A** twice, change one gain, and read the gap.
- **Part 6B:** `ambient 400` gives DNF; `thr 650` fixes it exactly (7.46 s). Put back `ambient 0`, `thr 300`.
- Shell settings last until reset. A manual lap never prints `$LAP` (but it can become the ghost).
- Expect slow motion in Wokwi (`world overruns` in `stats`). Lap times are world time, so they should still match the host.

## Wokwi steps

1. `build.bat` (or use the `Main.elf` already built). Open https://wokwi.com/projects/new/st-nucleo-c031c6, paste `diagram.json`, upload `Main.elf`.
2. Menu: joystick to `1 OVAL`, **A**, then **A** to start. Lap 1 should be about 5.20 s.
3. From lap 2 a ring appears at the start line and falls behind the robot. From lap 3 it rides on the triangle, and the bottom right shows the gap.
4. **A**, turn the knob down a bit, **A**: the ring now runs away from you. Turn it up: you pass it, and at the line it becomes the new ghost.
5. **SEL** for manual and chase it with the arrows.
6. `ghost 0` hides it; `stats` for the timing rows in the log below.

## Where it is in the code

| What | Where |
|---|---|
| ghost storage, 128 samples × 2 paths | `view.c:36` |
| the ring (XOR) | `view.c:156` `xor_ghost()` |
| record, keep the best, replay, lap gap | `view.c:169` `view_ghost()` |
| called after the HUD, 10 Hz | `Main.c:397` in `task_display` |
| shell `ghost 0/1` | `Main.c:526` |
| host test, table 10 | `host/sitl.c:315` |
| API and the comment | `view.h:23` |

## Your log: the "not watched in Wokwi" items (fill in during class)

| Item | Host / predicted | Wokwi says |
|---|---|---|
| Part 0: OVAL lap 1 / later laps, default knob | 5.20 s / 5.12 s | |
| `stats`: world step cycles (of 240 000) | ~200 000 on silicon | |
| `stats`: world overruns | 0 on silicon, many in Wokwi | |
| Menu: joystick up = previous track? | yes | |
| Part 3: S-BENDS knob 700, `kd 0` vs `kd 1` | 12.56 s vs 3.80 s | |
| Part 6B: HAIRPINS `ambient 400`, then `thr 650` | DNF, then 7.46 s | |
| Ghost: ring appears on lap 2 and trails the robot? | yes | |
| Ghost: gap after lap 3, OVAL knob 500 | about -0.00 (same lap) | |
| Ghost: still there after **A**, **A**? | yes | |
| Ghost: gap text overlaps `SLIP`/`RUN`? | no (starts at x 98) | |
| `stats`: slowest OLED flush with ghost on vs `ghost 0` | 1-2 more pages when the ring is away from the robot | |
| `stats`: display stack high-water of 256 words | frame barely changed | |
