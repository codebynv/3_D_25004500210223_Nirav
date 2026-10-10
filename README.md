# PTMAE — Pure Python Transactional Micro-Banking & Audit Engine

PTMAE is a Python 3 command-line assignment covering five units of the Python Programming course. It combines account-related calculations, manual log parsing, data transformations, in-place text-file updates, and object-oriented settlement rules.

The implementation uses only the permitted standard-library modules `datetime` and `random`; no third-party packages are required.

## Student

| Field | Details |
|---|---|
| Name | Nirav Vala |
| Semester | 3 |
| Division | D |
| Enrollment number | 25004500210223 |

## Units

1. **State control and trajectory guards:** nested command loop, iterative compound interest, periodic penalty calculation, and early-stop guards.
2. **Parser and closures:** index-based parsing, quoted delimiters, escaped quotes, closure state with `nonlocal`, and lambda late-binding protection.
3. **Data processing:** nested-comprehension reverse index and in-place queue cleanup.
4. **File processing:** `r+` record updates, chunked shifting when record lengths change, corruption logging, and ledger entries.
5. **Object-oriented settlement:** `Account`, Savings/Current/Credit subclasses, custom exceptions, balance validation, and isolated batch settlement.

## Files

- `main.py` — implementation and demonstration code for all five units.
- `documentation.md` — architecture and class diagrams, scope tracking, and the Units 1–5 checklist.
- `README.md` — project overview and run instructions.

## Run it in an interactive terminal

Open a terminal in the repository folder and run:

```bash
python main.py
```

The demonstration runs first, then the program asks for a command. Available commands:

```text
interest <principal> <rate> <years>
penalty <amount> <rate> [periods]
guard
exit
```

Examples:

- `interest 10000 5 2` prints `Computed Interest: 1025.00`.
- `penalty 10000 2` computes a one-period fee of `200.00`.
- `penalty 5000 2 3` computes `300.00` over three periods.

**VS Code note:** run this from **Terminal → New Terminal**, not from an output-only “Run Code” panel, because the interactive loop needs terminal input. If the input stream is unavailable, the script now detects EOF, prints a hint, and exits rather than looping forever.

## Runtime files

On first run, the program creates `accounts.db` if missing. File processing also writes `corrupted.log` for rejected records and `ledger.txt` for successful updates. These files are generated at runtime and are not part of the required submission folder.

See [`documentation.md`](documentation.md) for the architecture diagrams, state/scope table, and detailed compliance checklist.
