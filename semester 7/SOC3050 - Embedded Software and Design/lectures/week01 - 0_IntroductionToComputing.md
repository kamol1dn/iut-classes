# Chapter 0 — Introduction to Computing

**SOC3050 · Week 1 · 33 slides · Prof. Jeong Hong**
Source: [week01 - 0_IntroductionToComputing.pps](week01%20-%200_IntroductionToComputing.pps)
Deck credited to Sepehr Naimi (MicroDigitalEd) — the standard companion slides
for the AVR textbook this course follows.

> The file is in the **legacy binary `.pps` format**, which most tools can't
> read. To open or re-extract it:
> `soffice --headless --convert-to pptx "<file>"`

This is the groundwork chapter — the vocabulary for everything the course does
later with the ATmega.

**Topics:** internal organization of computers · memory · CPU · connecting the
parts with buses · how computers actually execute instructions.

---

## 1. The three parts of a computer

| Part | Role | Examples |
|---|---|---|
| **CPU** | Executes instructions | — |
| **Memory** | Stores, retains and recalls information | — |
| **I/O** | Input and output | **In:** keyboard, mouse, sensor · **Out:** LCD, printer, robot hands |

## 2. Memory

**Definition — deliberately broad:** anything that can **store, retain and
recall** information. A hard disk qualifies; so does a piece of paper.

### Three characteristics — likely exam question

| Characteristic | Meaning | Example |
|---|---|---|
| **Capacity** | The number of **bits** the memory can store | 128 Kbits, 256 Mbits |
| **Organization** | How the locations are arranged | A **128 × 4** memory = **128 locations of 4 bits each** |
| **Access time** | How long it takes to get data out | — |

> Capacity and organization are different things: a 128 × 4 and a 64 × 8 memory
> both hold 512 bits but are organised differently. Expect to be asked to
> compute one from the other.

### The semiconductor memory family

```
Semiconductor memory
├── RAM
│   ├── SRAM   (Static RAM)
│   ├── DRAM   (Dynamic RAM)
│   └── NV-RAM (Nonvolatile RAM)
└── ROM
    ├── Mask ROM
    ├── PROM   (Programmable ROM)
    ├── EPROM  (Erasable PROM)
    ├── EEPROM (Electrically Erasable PROM)
    └── Flash EPROM
```

### ROM types — distinguished by *how you erase them*

| Type | Programming / erasing |
|---|---|
| **Mask ROM** | Programmed by the **IC manufacturer**. You cannot change it. |
| **PROM** | **OTP — One-Time Programmable.** You can program it once. |
| **EPROM** (UV) | Erased by shining **ultraviolet light**. Takes **up to 20 minutes**, and erases the **entire contents**. |
| **EEPROM** | Erased **electrically** and **instantly**. Crucially, **each byte can be erased separately**. |
| **Flash ROM** | Erased "in a flash" — but the **entire device is erased at once**. |

> **The distinction that gets examined:** EEPROM erases **per byte**; Flash
> erases **the whole device**. That's the trade-off — Flash is faster and
> denser, EEPROM is finer-grained.

### RAM types — a three-way trade-off table

| | **SRAM** | **DRAM** | **NV-RAM** |
|---|---|---|---|
| **Built from** | Flip-flops (transistors) | **Capacitors** | SRAM + battery + control circuitry |
| **Advantages** | Faster · **no refresh needed** | Lower power · cheaper · **high capacity** | Very fast · infinite program/erase cycles · **non-volatile** |
| **Disadvantages** | High power consumption · expensive | **Slower · needs refreshing** | Expensive |

> **Why DRAM needs refreshing:** capacitors leak charge, so the contents must be
> periodically rewritten. Flip-flops hold their state as long as power is
> applied, which is why SRAM doesn't.

## 3. The CPU

**Its two tasks, as stated:**

1. **Execute instructions.**
2. **Recall the instructions one after another** and execute them.

### Inside the CPU — four components

| Component | Role |
|---|---|
| **PC — Program Counter** | Holds the address of the next instruction |
| **Instruction decoder** | Works out what the fetched instruction means |
| **ALU — Arithmetic Logic Unit** | Performs the arithmetic and logic |
| **Registers** | Fast internal storage (A, B, C, D in the example) |

## 4. Connecting everything — the bus

**The problem:** wiring each I/O device directly to the CPU means **the CPU
needs an enormous number of pins**. It doesn't scale.

**The solution — three shared buses:**

| Bus | Carries |
|---|---|
| **Address bus** | Which location is being accessed |
| **Data bus** | The actual data |
| **Control bus** | The operation — **Read** or **Write** |

Every device hangs off the same three buses, and the address plus control
signals determine which one responds.

### Two ways to attach I/O

| | **Peripheral I/O** | **Memory-Mapped I/O** |
|---|---|---|
| How it works | A dedicated **IO/MEM** control signal distinguishes an I/O access from a memory access | I/O devices simply **occupy addresses in the memory space** |
| Consequence | I/O has its own separate address space | I/O is read and written with ordinary memory instructions |

In the memory-mapped example, a **logic circuit enables the chip-select (CS)**
when the address falls in a given range — e.g. 0 to 15 for memory, with I/O
devices above that.

### Address decoding

The recurring design exercise, and a near-certain exam task:

1. Write out the address range in binary.
2. **Separate the fixed part** of the address — the high bits that don't change across the range.
3. **Design a logic circuit (typically a NAND) whose output activates when that fixed pattern appears.**

**His worked example:** design an address decoder for the range **300H – 3FFH**.
The low 8 bits vary across the range, so the fixed part is the upper bits
(`0011` for `a11 a10 a9 a8`) — decode those and you've selected the block.

> Practise this with a couple of other ranges. It's mechanical once you see that
> **the fixed part is whatever the start and end addresses have in common.**

## 5. How a computer actually executes a program

The deck traces a small program byte by byte, which is the most useful thing in
it. Memory holds a short sequence of instruction bytes at addresses 0–7, and
the CPU repeats the **fetch–decode–execute** cycle:

1. The **PC** supplies the address of the next instruction onto the **address bus**.
2. The instruction byte comes back over the **data bus**.
3. The **instruction decoder** splits it and works out the operation.
4. The **ALU** and **registers** carry it out — loading a value, adding two registers, storing a result back to memory.
5. The **PC increments**, and it repeats.

The traced program loads a value from an I/O address into register A, copies it
to B, loads a second value, adds them in the ALU, and writes the result back out
to memory — showing every bus transaction along the way.

### How the instruction decoder works

Each instruction byte splits into two fields:

```
| Opcode | Operand |
```

- The **opcode** (3 bits in this example, so **8 possible operations**) says *what to do*.
- The **operand** says *what to do it to* — an immediate value, a memory address, or a register.

The eight operations in the example cover the basic set you'd expect: load an
immediate value into A, load from a memory address, add and subtract (both
immediate and register forms), transfer between registers, and store A back to
memory.

> **The point being made:** machine code is not magic. An instruction is just a
> byte, split into "which operation" and "on what", and the decoder is a lookup.
> This is the mental model you need before writing AVR assembly.

## 6. Von Neumann vs Harvard architecture

The last slide, and a guaranteed exam question:

| | **Von Neumann** | **Harvard** |
|---|---|---|
| Buses | **One** set of address/data/control buses | **Two separate** sets |
| Memory | Code and data share the **same** memory space | Code memory and data memory are **separate**, each with its own buses |
| Consequence | Simpler and cheaper; but fetching an instruction and fetching data **compete for the same bus** | Instruction and data can be fetched **simultaneously** — faster |

> **Why this matters for this course:** the **AVR is a Harvard architecture**
> machine. That's why Flash (program) and SRAM (data) are addressed separately
> on the ATmega, and why you'll see distinct instructions for reading program
> memory versus data memory.

---

## If you're revising this in 10 minutes

1. **Three memory characteristics** — capacity, organization (128 × 4 = 128 locations of 4 bits), access time.
2. **ROM ladder** — Mask (factory) → PROM (once) → EPROM (UV, 20 min, all) → EEPROM (electrical, instant, **per byte**) → Flash (**whole device at once**).
3. **SRAM vs DRAM** — flip-flops vs capacitors, and therefore fast/power-hungry vs slow/needs-refresh.
4. **The three buses** and why a bus exists at all (pin count).
5. **Peripheral vs memory-mapped I/O.**
6. **Address decoding** — find the fixed high bits, NAND them. Try the 300H–3FFH example yourself.
7. **PC / instruction decoder / ALU / registers**, and the fetch–decode–execute cycle.
8. **Von Neumann vs Harvard**, and that **AVR is Harvard**.

## Where the rest of this course lives

eClass has almost nothing else for SOC3050 — the working material is on
**GitHub** and **Telegram**. See the [course README](../README.md).
