# Midterm session 1: lessons 00–03 (Part 0, "models")

Sun 2026-10-18, about 21:00–23:30. The exam is 60 min, 33 MCQ, closed book, lessons 00–08.
Tonight covers the four "models" lessons, worth roughly **12–15 of the 33 questions**.

Material, in [`labs/soc3050code/projects2026_arm/`](../labs/soc3050code/projects2026_arm/):
- **Study guide** [`exam_midterm/overview.md`](../labs/soc3050code/projects2026_arm/exam_midterm/overview.md):
  §2 *Key contrasts* (line ~80) and §3 lesson notes 00–03 (lines 103–503, about 3,000 words)
- **Decks:** `00_Architecture/Slide.md` · `01_Instruction_Set/Slide.md` · `02_Development/Slide.md` · `03_Execution_Concurrency/Slide.md`
  (also on https://gnoejh.github.io/soc3050code/)

## Timeline

| Time | Do | |
|---|---|---|
| 21:00–21:15 | Read guide **§1–2**: the exam format and the **Key contrasts** table. Say each pair out loud: the two options, which one this chip uses, and what follows from it | ☐ |
| 21:15–21:50 | Guide **Lesson 00** (the programmer's model) + **01** (instruction set). Open the deck slide whenever the guide cites one | ☐ |
| 21:50–22:00 | Break | |
| 22:00–22:35 | Guide **Lesson 02** (development, linker, sections) + **03** (execution, concurrency, `volatile`) | ☐ |
| 22:35–23:20 | **Self-check below**, out loud, without looking. Mark each ✗ or ?, then look up only those | ☐ |
| 23:20–23:30 | Practice **P10, P11, P12** from guide §6 (the ones that use lessons 00–03). Check them against the answers | ☐ |

**On paper by hand, no calculator:** a 32-bit hex value written as little-endian bytes,
a Thumb address with bit 0 set (`0x08000275` → the function is at `…274`), and a vector address
(`0x08000000 + 4 × vector`).

## Self-check (the decks' own "What You Should Be Able to Say" slides)

### 00 — The Programmer's Model
1. What does a *programmer's model* include, and what does it deliberately leave out?
2. Name its five parts for this chip.
3. The CPU has one mechanism for reaching anything outside itself. What is it?
4. Three ways a register behaves differently from a variable.
5. The three roles of peripheral registers, and who writes each.
6. Which peripherals are ARM's and which are ST's? Why does that decide which manual you open?
7. You configure a peripheral and it reads back as zero. What's your first suspect?
8. Serial output is garbage but the code is right. Give two causes.
9. You cast a `uint8_t*` to a `uint32_t*` and the chip HardFaults. Why? Would a Cortex-M3 fault too?
10. The three places the implementation leaks into code you must write.
11. How does the hardware find the function you wrote for USART2?
12. The two ways a processor lets software reach a device. Which did the AVR use, and which does this chip use?
13. What does *Harvard* mean, and which AVR keyword existed only because of it?
14. A desktop stops a bad pointer with a segfault. What hardware does that? What does this chip have instead, and what does a bad pointer do here?

### 01 — Instruction Set
1. Roughly how many distinct instructions make up 80% of firmware?
2. Why does setting one bit in a peripheral register take at least three instructions?
3. What does `bics` do, and which C operator produces it?
4. Why is `lsls` more common than `subs` in embedded code?
5. `cmp` subtracts and discards the result. What is the point?
6. `blt` vs `bcc`: what's the difference, and what bug comes from confusing them?
7. What does `pop {r4, pc}` do that `pop {r4, lr}` doesn't?
8. Which addressing mode is `s->field`? Which is `buf[i]`?
9. Why is there no divide instruction, and how does a `.map` file show your code divided?
10. ARM's other instruction set: what's its name, and when does a Cortex-M switch to it?
11. Three things a Cortex-M4 does in one instruction that this M0+ can't.
12. The reset vector holds `0x08000275` but the function is at `0x08000274`. Why, and what happens if you "fix" it?
13. `LR` reads `0x0800028f` at a breakpoint. Which instruction runs on return? What would an **even** `LR` tell you?
14. The two instruction-set models. Which one is this chip, which is x86, and which was the AVR?
15. RISC-V has no flags register. How does it write `if (a < b) goto L`, and what does ARM gain by having one?
16. The two ways to remember a return address. Which does this chip use, and what is `push {lr}` really for?
17. Why can't a 16-bit instruction load `0x40021000`? Give ARM's answer and one other machine's.

### 02 — Development
1. The five stages of a build. Which one is embedded-specific?
2. Where does `.data` live, flash or RAM? Defend your answer.
3. What are `_sdata` and `_ebss`, and who creates them?
4. What happens if the `.bss` loop is missing? Why is the bug intermittent?
5. Which two numbers in the linker script come from the datasheet, and what goes wrong if they're too large?
6. The hex file begins `:02000004 0800`. What is that record for, and why did 8-bit chips never need one?
7. The three moments a name can be bound to an address. Which does this chip use, which does your laptop use, and what hardware does the laptop need for it?
8. Why does 364 B of `.bss` cost nothing in flash, while 96 B of `.data` costs 96?
9. The boot chain of a PC vs this chip: how many handoffs does each have?

### 03 — Execution and Concurrency
1. The three ways to meet hardware. Give a case where polling is the right choice.
2. Why can an ISR here be an ordinary C function with no special keyword?
3. What exactly does `volatile` prevent? Name one thing it does **not** do.
4. Draw the instruction sequence that loses an update to a shared counter.
5. A single aligned `uint8_t`, written only by the ISR and read only by main: does it need a critical section? Why?
6. Why must interrupt handlers be short?
7. A program works for hours, then misbehaves once. What class of bug is this, and why won't running it more help?
8. State the as-if rule in one sentence, and say why hardware breaks its assumption.
9. Define *race condition*, *critical section*, *mutual exclusion* and *atomic* without mentioning ARM.
10. Why is `__disable_irq()` not enough on a dual-core chip, and what replaces it?
11. What is *tearing*, and which two rows of the lesson-03 slide-7 table are instances of it?

## My ✗ / ? list

(Write the question numbers you couldn't answer. Next session starts with these.)

-
