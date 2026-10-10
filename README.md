# PTMAE — Pure Python Transactional Micro-Banking & Audit Engine

PTMAE is a Python 3 command-line assignment covering the five required units of the Python Programming SRS. It demonstrates loop-based calculations, manual parsing, closures, reverse indexing, in-place queue processing, record updates with `r+`, error logging, and polymorphic account settlement.

## Student

| Field | Details |
|---|---|
| Name | Nirav Vala |
| Semester | 3 |
| Division | D |
| Enrollment number | 25004500210223 |

## Units covered

1. **State control and trajectory guards** — nested `while` loops, compound interest, penalty fees, and early termination on a threshold or `STOP` flag.
2. **Parser and closures** — index-based parsing of quoted fields and escaped quotes, `nonlocal` state, and lambda filters bound with `k=k`.
3. **Data inversion and queue processing** — a sorted reverse index and in-place list/tuple/set/primitive cleanup.
4. **File processing and exceptions** — `r+` account updates, chunked shifting when record length changes, `corrupted.log`, `ledger.txt`, and custom exceptions.
5. **Object-oriented settlement** — `Account`, `SavingsAccount`, `CurrentAccount`, `CreditAccount`, balance validation, name mangling, and isolated batch settlement.

## Repository files

- `main.py` — implementation, interactive menus, built-in demonstration, and live self-audit.
- `documentation.md` — architecture and class diagrams, state/scope table, and the Units 1–5 checklist.
- `README.md` — overview and run instructions.

## Run

Open a terminal in the repository folder and run:

```bash
python main.py
```

The program opens a grouped menu. Enter `0` to exit. Useful options are `1` for interest and penalty calculations, `8` for file processing, `10` for the command shell, `11` for the full demonstration, and `13` for the self-audit.

In the command shell (option `10`), enter one command per line:

```text
interest 10000 5 2
penalty 50 10
guard 1000 500 -300 -300 -300 50
exit
```

Expected results include compound interest `1025.0`, a ten-day penalty of `650`, and a guarded final balance of `400.0`. The penalty command uses `penalty <base_fee> <days_late>`.

Run the program in an interactive terminal, such as **VS Code → Terminal → New Terminal**, so it can receive keyboard input. If no input stream is available, the program runs the demonstration and self-audit, then exits rather than looping on `EOFError`.

## Runtime files

The file-processing demo creates or resets `accounts.db` and writes `corrupted.log` and `ledger.txt`. The self-audit uses separate `audit_*.tmp` files. These are runtime artifacts, not required source files for the submission ZIP.

See [`documentation.md`](documentation.md) for the detailed design and compliance checklist.