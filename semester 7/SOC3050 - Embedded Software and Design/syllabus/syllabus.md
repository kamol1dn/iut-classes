# SOC3050 — Embedded Software & Design

> Official syllabus, 2026 Fall Semester. Mirrored from eClass on 2026-09-20.
> Source: `https://eclass.inha.ac.kr/local/ubion/setting/syllabus.php?id=2615`
> Original PDF: [soc3050.pdf](soc3050.pdf)

| | |
|---|---|
| **Course No.** | SOC3050 — Class 001 |
| **Semester** | 2026 Fall (202602) |
| **Instructor** | Jeong Hong |
| **Room** | B-101 |
| **Schedule** | Wed `15~17` · Fri `18~20` (as registered — see note below) |
| **Credits** | 3.0 |
| **Grading** | Relative evaluation |
| **Mode** | Offline |

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

The `Schedule` row reproduces the eClass syllabus field verbatim. eClass is
ambiguous about whether those numbers are clock hours or period (교시) indices:
the upcoming-events calendar labels the same classes with different period
numbers (e.g. a Monday DLCV class appears as `4교시` while the syllabus says
`14~16`). Treat the numbers as the registered values, and confirm actual
start times against the timetable image in `resources/` or with the instructor.
