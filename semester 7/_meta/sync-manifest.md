# eClass sync manifest

Everything needed to re-check this semester without re-discovering the site.
**Last full sync: 2026-09-20.**

Base URL: `https://eclass.inha.ac.kr`

## Useful endpoints

| Purpose | Path |
|---|---|
| Course page | `/course/view.php?id=<COURSE_ID>` |
| Syllabus (structured) | `/local/ubion/setting/syllabus.php?id=<COURSE_ID>` |
| File download (direct) | `/mod/ubfile/view.php?id=<MOD_ID>` |
| Board listing | `/mod/ubboard/view.php?id=<MOD_ID>` |
| Board post | `/mod/ubboard/article.php?id=<MOD_ID>&bwid=<POST_ID>` |
| VOD | `/mod/vod/view.php?id=<MOD_ID>` |
| Quiz | `/mod/quiz/view.php?id=<MOD_ID>` |
| Upcoming events | `/calendar/view.php?view=upcoming` |
| Grades | `/grade/report/user/index.php?id=<COURSE_ID>` |
| Offline attendance | `/local/ubattendance/my_status.php?id=<COURSE_ID>` |

Notes for re-syncing:
- `/mod/ubfile/view.php?id=N` returns the file itself with a
  `Content-Disposition` filename — not an HTML page.
- Course pages render the current week twice (once in a "Current week course"
  block, once in the full list). De-duplicate by section name.
- The platform is Moodle-based with `ubfile` / `ubboard` / `vod` custom modules.

## Course IDs

| Course | eClass id | Announcements | Q&A |
|---|---|---|---|
| NTS4070 Distinguished Lecture in Social Science and Art | 2592 | 69948 | 69949 |
| SOC3050 Embedded Software & Design | 2615 | 69794 | 69795 |
| SOC4020 Multimedia Computing | 2622 | 70064 | 70065 |
| SOC4040 Artificial Intelligence | 2626 | 69586 | 69587 |
| SOC4180 Deep Learning for Computer Vision | 2634 | 69602 | 69603 |
| SOC4190 Blockchain Basics and Platforms | 2635 | 70114 | 70115 |

## Files mirrored (module id → local path)

### NTS4070 (course 2592)

| Mod | Original filename | Bytes | Local path |
|---|---|---|---|
| 70105 | Syllabus - Distinguished.pdf | 233,060 | `syllabus/Syllabus - Distinguished Lecture.pdf` |
| 70106 | DLSSA 1.pptx | 270,321 | `lectures/week01 - DLSSA 1 (class intro + lecture 1).pptx` |
| 70700 | DLSSA 2.pptx | 126,446 | `lectures/week02 - DLSSA 2.pptx` |
| 71121 | DLSSA 3.pptx | 82,640 | `lectures/week03 - DLSSA 3.pptx` |

Non-downloadable (must be used on eClass): VOD 70109, 70112, 70704, 71123,
71124; Quiz 70117, 71122.

### SOC3050 (course 2615)

| Mod | Original filename | Bytes | Local path |
|---|---|---|---|
| 69796 | soc3050.pdf | 450,614 | `syllabus/soc3050.pdf` |
| 70043 | 0_IntroductionToComputing.pps | 1,033,728 | `lectures/week01 - 0_IntroductionToComputing.pps` |
| 71126 | Class0918.png | 120,626 | `resources/timetable - Class0918.png` |

External: URL mod 69798 → https://github.com/gnoejh/soc3050code ·
URL mod 70977 → https://t.me/+EcqPs3qT0oZjYTI6

### SOC4020 (course 2622)

| Mod | Original filename | Bytes | Local path |
|---|---|---|---|
| 70066 | Multimedia Computing_L1 (3).pptx | 25,166,887 | `lectures/week01 - Multimedia Computing L1.pptx` |
| 70527 | Multimedia Computing L2 (2).pptx | 3,341,122 | `lectures/week01 - Multimedia Computing L2.pptx` |
| 70885 | Multimedia Computing L3 (3).pptx | 1,534,366 | `lectures/week02 - Multimedia Computing L3.pptx` |
| 70938 | Multimedia Computing L4_update (2).pptx | 1,624,543 | `lectures/week02 - Multimedia Computing L4 (update).pptx` |
| 70886 | practice code_L3 (4).rar | 2,545,840 | `resources/practice code L3.rar` |

### SOC4040 (course 2626)

| Mod | Original filename | Bytes | Local path |
|---|---|---|---|
| 70515 | 1.1. Intro to AI.pdf | 9,342,810 | `lectures/week01 - 1.1. Intro to AI.pdf` |
| 71098 | 1.2. Intro to Machine Learning.pdf | 4,185,455 | `lectures/week01 - 1.2. Intro to Machine Learning.pdf` |
| 71099 | 2.1. Intro to Machine Learning.pdf | 2,495,664 | `lectures/week02 - 2.1. Intro to Machine Learning.pdf` |
| 71100 | 2.2. Logistic Regression.pdf | 2,552,744 | `lectures/week02 - 2.2. Logistic Regression.pdf` |
| 71101 | linear_regression.ipynb | 357,628 | `resources/linear_regression.ipynb` |
| 71102 | logistic_regression.ipynb | 164,173 | `resources/logistic_regression.ipynb` |

Announcement 69586 / post 7634 — "Discord server invite link", Mamurov Jasurbek,
2026-09-17: https://discord.gg/tWQUXMpM7

### SOC4180 (course 2634)

| Mod | Original filename | Bytes | Local path |
|---|---|---|---|
| 69793 | soc4180.pdf | 453,642 | `syllabus/soc4180.pdf` |
| 71125 | Class0918.png | 120,626 | `resources/timetable - Class0918.png` |

External: URL mod 69797 → https://github.com/gnoejh/soc4180 ·
URL mod 70976 → https://t.me/+UHxHay2_c3kyMGQy ·
URL mod 70981 → https://gnoejh.github.io/soc4180/

### SOC4190 (course 2635)

Nothing published. Only the two auto-created boards exist.

## State captured at last sync

- NTS4070 attendance: week 1 ✅ · week 2 ✅ · week 3 ✅ (3 attendance, 0 absences, 0 late)
- Announcement posts across all six courses: **1** (the SOC4040 Discord link)
- Assignments (`mod/assign`) configured anywhere: **0** — every course sets
  homework in class or off-platform, not through the eClass assignment module

### Activity counts — the cheap way to detect new material

Fetch `/course/view.php?id=N` and count `li.activity`. If the number is
unchanged, nothing was posted and there is no need to crawl the sections.

| Course | 2592 | 2615 | 2622 | 2626 | 2634 | 2635 |
|---|---|---|---|---|---|---|
| Activities @ 2026-09-20 11:33 | 17 | 7 | 7 | 8 | 7 | 2 |

(2592 counts 17 because the course page renders the current week twice.)

## EduPage timetable

Separate system from eClass, public, no login:

| | |
|---|---|
| Page | `https://iut.edupage.org/timetable/` |
| List timetables | POST `/timetable/server/ttviewer.js?__func=getTTViewerData` |
| Full dataset | POST `/timetable/server/regulartt.js?__func=regularttGetData` |
| Class | `ICE23-1` (EduPage id `*77`) |
| Timetable in use | `145` — Fall_2026 (7/9 – 27/12/2026) |

Both endpoints need a `PHPSESSID` from a prior GET on `/timetable/`, take
exactly two positional `__args`, and accept `__gsh: "00000000"`. The second
argument to `getTTViewerData` is the **school year**; pass the wrong thing and
it still returns the list but leaves `default_num` blank.

Periods are 30-minute slots from 08:00 — period *n* starts at `07:30 + 0:30n`.
This is the same numbering the eClass syllabi use.

Known discrepancy: eClass registers **SOC3050 Friday as `18~20` in B-101**;
EduPage says **`13~15` (14:00–15:30) in B202**. All 7 other slots agree.

Regenerate with `python scripts/pull_timetable.py`.

## Lecture VODs

The video player at `/mod/vod/viewer.php?id=<MOD>` embeds a Wowza HLS stream on
`vod.inha.ac.kr:8443`. The stream URL is present in that page's HTML — no need
to press play. The **stream endpoints need no credentials**; only discovering
the URL requires a logged-in eClass session.

Cached in `scripts/vods.json`; download with `scripts/pull_vods.py` (ffmpeg
`-c copy`, so no re-encode), transcribe with `scripts/transcribe_vods.py`.

| Mod | Week | Title | Length | Size |
|---|---|---|---|---|
| 70109 | 1 | Class intro | 18:09 | 60 MB |
| 70112 | 1 | Lecture 1 | 44:35 | 152 MB |
| 70704 | 2 | Lecture 2 | 1:00:34 | 140 MB |
| 71123 | 3 | Lecture 2-1 | 38:22 | 94 MB |
| 71124 | 3 | Lecture 3-2 | 25:35 | 80 MB |

To refresh when new lectures appear: open each VOD's `viewer.php` on a logged-in
session, regex the HTML for `playlist.m3u8`, and add an entry to `vods.json`.

Gotchas:
- `.mp4`/`.wav`/`.words.json` are git-ignored; `.srt`/`.txt`/`.md` are tracked.
- Transcription runs Captioneer (`D:\coding\captioneer-english`) via its own
  venv — it is an MCP server but is **not connected to this session**.
- Its CLI prints non-ASCII and dies on the cp1252 console; set
  `PYTHONIOENCODING=utf-8`.
- large-v3 + WhisperX nearly fills 8 GB VRAM. Back-to-back runs can OOM before
  the previous process releases memory; the script waits and retries. **Never
  run two transcriptions at once.**

## Sync log

| When | Result |
|---|---|
| 2026-09-20 11:10 | Initial full mirror — 20 files. NTS4070 at 1 attendance / 2 absences. |
| 2026-09-20 11:33 | Attendance + deadlines re-check. NTS4070 now 3 / 0. No new material in any course. |
| 2026-09-20 13:42 | Added EduPage timetable puller. Resolved the period numbering, found the SOC3050 Friday discrepancy, excluded dropped BDA. |
| 2026-09-20 19:05 | Downloaded all 5 NTS4070 VODs (526 MB), transcribed with whisper large-v3, wrote summaries. Surfaced the 3-absence limit, the quiz policy, and an unposted quiz question. |
