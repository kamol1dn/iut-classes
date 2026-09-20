# SOC3050 — Embedded Software & Design

> Official syllabus, 2026 Fall Semester. Mirrored from eClass on 2026-09-20.
> Source: `https://eclass.inha.ac.kr/local/ubion/setting/syllabus.php?id=2615`
> Original PDF: [soc3050.pdf](soc3050.pdf)

| | |
|---|---|
| **Course No.** | SOC3050 — Class 001 |
| **Semester** | 2026 Fall (202602) |
| **Instructor** | Jeong Hong |
| **Room** | B-101 (Wed) · **B202 (Fri)** |
| **Schedule** | Wed **15:00–16:30** (B101) · Fri **14:00–15:30** (**B202**) — see warning below |
| **Credits** | 3.0 |
| **Grading** | Relative evaluation |
| **Mode** | Offline |

## ⚠️ eClass has the Friday slot wrong

The eClass syllabus registers Friday as periods `18~20` (17:30–19:00) in B-101.
The official EduPage timetable puts it at periods **13~15, i.e. 14:00–15:30, in
B202** — a different time *and* a different room. Every other slot across all
four offline courses matches; this is the only discrepancy.

**Trust the timetable, not the syllabus, for Friday.** Given that this course
closes the door 5 minutes after the start and 8 absences fails you, it is worth
confirming with Prof. Jeong Hong directly.

## Grading breakdown

| Mid-term | Final | Attendance | Assignments | Quiz | Discussion | Etc. |
|---|---|---|---|---|---|---|
| 30% | 30% | 5% | 30% | 0% | 0% | 5% |

## Course objectives

Foundational, hands-on introduction to embedded systems, from microcontroller
architecture to intelligent real-world applications. Students program embedded
hardware in Assembly and C/C++, interface sensors and actuators, control
real-time systems, and deploy lightweight deep learning models for embedded
intelligence.

Covers representative processor families — AVR ATmega, Intel-based
microcontrollers and others — supported through simulation environments such as
SimulIDE and RTOS frameworks. Students gain experience in both bare-metal
programming and OS-based development, understanding how processor architecture,
memory organization, interrupts and peripherals shape embedded software design.

Weekly lectures plus laboratory sessions build and test embedded applications
connected to a computer, culminating in practical systems such as drones, mobile
robots and autonomous devices.

## Course description

**Embedded fundamentals** — AVR architecture and memory organization; instruction
set, control flow and low-level execution; microcontroller design principles.

**Programming techniques** — timers and real-time scheduling; interrupt handling
and event-driven control; serial communication (UART, SPI, I²C).

**Hardware interfacing** — LCD modules and display control; analog/digital
sensors and signal acquisition; motor drivers, PWM and actuator control;
analog/digital I/O management.

**Embedded intelligence** — embeddings and lightweight representation learning;
attention mechanisms adapted for constrained devices; TinyML deployment on
microcontrollers.

**Project integration** — IoT system design and communication; automation and
control applications; AI-enhanced embedded systems (vision, decision-making).

**Tools & languages** — SimulIDE and hardware emulation; ATmega development
boards; Assembly programming; C/C++ for embedded software engineering.

## Class structure

Lecture · Labs · Project · Exams

## Weekly plan

| Week | Theme | Details | Lab |
|---|---|---|---|
| 1 | Embedded Systems Overview | Introduction to computing principles, AVR microcontroller overview, hardware/software integration concepts | |
| 2 | AVR Architecture & Programming | Internal architecture, register operations, instruction set fundamentals, activation logic, optimization strategies | Lab |
| 3 | Control Flow | Branching, subroutine calls, delay loops for timing control | Lab |
| 4 | Advanced Instructions | Arithmetic and logic operations, residual connections, normalization techniques in embedded contexts | Lab |
| 5 | AVR I/O Port Programming | Digital I/O configuration, bit-level manipulation, port-based device control | |
| 6 | Deep Learning in Embedded Systems | TinyML, deploying lightweight models, sensor-driven inference on microcontrollers | |
| 7 | **Midterm Exam** | Covers weeks 1–6, theory and practical lab components | Lab |
| 8 | Timer Programming | Timer modes, counters, PWM, real-time scheduling | |
| 9 | Interrupt Programming | Interrupt service routines (ISRs), external and internal triggers | Lab |
| 10 | Serial Communication | UART configuration, serial data transmission, debugging techniques | Lab |
| 11 | Display & Input Devices | LCD displays and matrix keypads | Lab |
| 12 | Analog Interfacing | Analog sensors via ADC/DAC, signal conditioning, data acquisition | Lab |
| 13 | Actuator Control | Relays, optoisolators, stepper motors | Lab |
| 14 | Project Presentation | Student-led demonstrations of embedded projects | |
| 15 | **Final Exam** | Covers weeks 8–13, system design and interfacing | |
| 16 | Makeup | | |

## ⚠️ Failure conditions (from the syllabus notes)

Any **one** of the following results in failure:

- **Attendance:** 1/4 of classes absent (8 times), unless admitted beforehand by
  the instructor (not by AA).
- No Labs, No Project, No Midterm exam, or No Final exam.
- Cheating in labs, homeworks, projects or exams.
- Other activity harming the course.
- **Class door is closed 5 minutes after class starts.**

No class change allowed. Course contents may be changed and updated during the
semester; evaluation criteria may vary depending on circumstances.

---

## Note on the schedule numbers

**Resolved.** The eClass syllabus numbers are **period indices**, and periods are
30-minute slots starting at 08:00 — so period *n* begins at `07:30 + 0:30n`, and
a `a~b` range runs from the start of period *a* to the end of period *b*.

Verified against the official EduPage timetable for ICE23-1, which agrees with
eClass on 7 of the 8 registered slots. The clock times in the table above are
the authoritative ones, taken from [../../timetable.md](../../timetable.md) —
regenerate it with `python scripts/pull_timetable.py`.
