# Lab 07b: Learning a table from experience

Repo: `labs/soc4180/weeks/07b-tabular/`. **You edit only `tables.py`.** `lab_tables.py` is the
referee. Its scorer code must read **119A**; any edit to it changes the code.

`tables.py` already contains the reference answers and scores 6/6. The lab is to run it,
understand why each answer is right, then break answers on purpose and watch what fails.

## Run it

From `labs/soc4180` (use the venv's Python directly: `uv run --extra rl` would re-sync the venv
and download torch):

```bash
.venv/Scripts/python.exe weeks/07b-tabular/lab_tables.py
```

Keys (click the MuJoCo window first; if no key works there, press them in the terminal):
`1`–`6` play a problem (training is live, and the arrows show the table's best action), `SPACE` replays,
**`G` grades all six** (about 2 min; the score and scorer code stay on screen), `ENTER` prints the gauge,
and `q` quits. On problem 5, after training, ctrl + right-drag the pole to push it.

Headless check: `.venv/Scripts/python.exe weeks/07b-tabular/lab_tables.py --grade --no-viewer`

**To do:** set `NAME = "..."` in `tables.py`, press `G`, and show the instructor 6/6 with code 119A.

## The one rule

    Q[s,a] += alpha * (target - Q[s,a])
    Q-learning: target = r + gamma * max_a' Q[s',a']   (off-policy: a' = the greedy action)
    SARSA:      target = r + gamma * Q[s',a']          (on-policy: a' = the action it will actually take)

Off- vs on-policy test: is the a' in the target chosen by the same policy that chose a
(ε-greedy)? SARSA: yes, so it's on-policy. Q-learning: no (it uses argmax), so it's off-policy.
Value iteration (week 7) needs P. These two need only samples (s, a, r, s').

## Why each answer

| # | Problem | Answer | Why |
| --- | --- | --- | --- |
| 1 | FAR-SIGHTED (lake) | `gamma 0.99` | The safe route round the holes is long. With a low γ a distant reward is worth almost nothing, so the routes' values squeeze together and noisy samples can't separate them. Fails at 0.5, 0.9 and 0.95. |
| 2 | WATCHER (random actions) | `"q"` | Off-policy: its target uses the best next action whatever it actually did, so it learns Q* from random behaviour. SARSA learns the value of acting randomly, which is useless to follow greedily. |
| 3 | SAFE (cliff, exploring) | `"sarsa"` | On-policy: its values include its own 10 % random slips, so it learns that the edge is dangerous and takes the path up and over (17 steps, few falls). |
| 4 | SHORT (cliff greedy path) | `"q"` | It learns the greedy-optimal path along the edge (13 steps). It falls often while exploring, but the grade looks only at the greedy path. |
| 5 | PENDULUM | angle + angular velocity, 6×6 = 36 rows | The angle alone isn't a state (not Markov: you can't tell if the pole is falling). All four numbers give 324 rows, too many to fill in 3000 episodes. |
| 6 | G1 BALANCE | `bins 21` | An inverted U. 5 or 11 bins are too coarse (one row lumps states that need different actions). 81 bins are visited too rarely. 21 and 41 pass (J 65.5 and 66.1 against π* 72.12). |

## Break it (predict first, then play that number)

- P1 `gamma 0.5`: success about 7 %. The arrows stop leading round the holes.
- P2 `"sarsa"`: greedy success 13–61 %, fails 60 %.
- P3 `"q"`: 47–51 falls in the last 200, fails < 25.
- P4 `"sarsa"`: path 17–19 steps, fails 13.
- P5 only `"pole angle"`: 7–35 steps. Add all four numbers: 43–77 steps.
- P6 `bins 5`, `11` or `81`: J 19.1, 51.1 or 53.3, all under 60.

Put `...` in place of an answer to blank it, and the game names the line. Restore the reference
before you get graded.

Checked on this laptop 2026-11-12: problem 1 passes (0.737, the same as π*), and the scorer code is 119A.
