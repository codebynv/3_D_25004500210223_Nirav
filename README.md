# PTMAE — Pure Python Transactional Micro-Banking & Audit Engine

PTMAE is a Python 3 command-line assignment covering the five required units of the Python Programming course. It brings together account-related calculations, manual log parsing, data transformations, in-place text-file updates, and object-oriented settlement rules.

The implementation uses the permitted standard-library modules `datetime` and `random`; it does not require third-party packages.

## Student

| Field | Details |
|---|---|
| Name | Nirav Vala |
| Semester | 3 |
| Division | D |
| Enrollment number | 25004500210223 |

## Units covered

| Unit | Main topics |
|---|---|
| **1. State control and trajectory guards** | Nested command loop, compound interest, penalty calculation, and early-stop guards |
| **2. Log parser and closures** | Index-based parsing, quoted delimiters, escaped quotes, closure state with `nonlocal`, and lambda late-binding protection |
| **3. Data inversion and in-place processing** | Nested-comprehension inversion, in-place queue cleanup, tuple conversion, set filtering, list sorting, and duplicate removal |
| **4. File modifier and error logger** | `r+` database updates, chunked shifting when record lengths change, corrupted-record logging, and ledger entries |
| **5. Object-oriented settlement engine** | Base `Account`, Savings/Current/Credit accounts, custom exceptions, balance validation, and isolated batch settlement |

## Files

- **`main.py`** — implementation and demonstration for Units 1–5.
- **`documentation.md`** — architecture and class diagrams, state/scope table, and unit-by-unit compliance checklist.
- **`README.md`** — project overview and run instructions.

## Run the program

Use Python 3 from the repository root:

```bash
python main.py
```

The script runs the demonstrations first and then opens the interactive command loop. Available commands are:

```text
interest <principal> <rate> <time>
penalty <amount> <rate>
guard
exit
```

For example, enter `interest 10000 5 2` to calculate the compound interest for a principal of 10000 at 5% for 2 years.

## Runtime files

On its first run, the program creates `accounts.db` if the file is missing. The file-processing demonstration also writes `corrupted.log` for rejected records and `ledger.txt` for accepted updates. These are generated at runtime and are not required in the repository's source files.

The account database is updated during execution, so its contents can change between runs. Remove the generated `accounts.db` when a fresh first-run demonstration is needed.

For the architecture diagrams, scope tracking, and full Units 1–5 checklist, see [`documentation.md`](documentation.md).
