# PTMAE — Pure Python Transactional Micro-Banking & Audit Engine

A Python 3.x command-line project built for the **Python Programming (Units 1–5)** assignment.

PTMAE combines a small banking engine with audit and file-processing exercises. The project is intentionally implemented with core Python constructs rather than external packages, so the code itself demonstrates the concepts required by the assignment.

## Student

| Field | Details |
|---|---|
| Name | **Nirav Vala** |
| Semester | 3 |
| Division | D |
| Enrollment No. | 25004500210223 |
| Language | Python 3.x |

---

## What the project does

PTMAE covers five main areas:

- **Interactive command processing** for interest calculation and transaction trajectory checks.
- **Manual log parsing** that handles quoted fields, delimiters inside quotes, escaped quotes, empty fields, and trailing fields.
- **Data processing** using comprehensions, in-place list operations, set operations, sorting, and duplicate removal.
- **Transactional file updates** on `accounts.db` using `r+`, `tell()`, `seek()`, chunked shifting, and `truncate()`.
- **Object-oriented account settlement** using inheritance, encapsulation, custom exceptions, and polymorphism.

The project does not use a database server, web framework, or third-party package.

---

## Project structure

```text
ptmae-python-assignment/
│
├── main.py             # Complete PTMAE implementation
├── Documentation.md    # Architecture, scope tracking, and requirement mapping
├── SRS-PY3 (1).md      # Assignment Software Requirements Specification
├── accounts.db         # Seed account records used by the file-processing module
└── .gitignore          # Ignores runtime and test-generated files
```

During execution, the program can create/update:

```text
corrupted.log          # Rejected/corrupted records
ledger.txt             # Successfully processed account updates
```

These runtime files are intentionally ignored by Git.

---

## Requirements

- Python **3.x**
- No pip installation required
- Only the modules permitted by the assignment are used:
  - `datetime`
  - `random`

The program is designed to run from the project directory.

---

## Running the project

Clone the repository and enter the project directory:

```bash
git clone https://github.com/codebynv/ptmae-python-assignment.git
cd ptmae-python-assignment
```

Run:

```bash
python main.py
```

On Windows, `py main.py` can also be used if the Python launcher is configured.

The demonstration section runs first and then starts the interactive command loop.

---

## Interactive commands

Once the interactive prompt appears:

### Compound interest

```text
PTMAE> interest 10000 5 2
```

Format:

```text
interest <principal> <rate> <time>
```

The calculation is performed directly with Python arithmetic operators; no math library is used.

### Trajectory guard

```text
PTMAE> guard
```

This demonstrates early termination when the transaction trajectory reaches the configured safety condition or termination flag.

### Exit

```text
PTMAE> exit
```

Ends the interactive loop.

---

## Main modules

### 1. State Control Engine

The first part of the program demonstrates:

- nested `while`-based command processing
- manual command parsing
- compound interest calculation
- trajectory-based balance checking
- short-circuit `or` logic
- early termination of transaction processing

### 2. Native Log Parser & Closures

`parse_raw_log_line()` is written as a character-by-character parser instead of using `split()` or `replace()`.

It handles:

- quoted fields
- delimiters inside quoted fields
- escaped quotes
- empty fields
- trailing delimiters

The same module also demonstrates:

- closures
- `nonlocal` state
- lambda functions created inside a loop
- default-argument binding to avoid late-binding problems

### 3. Data Inversion & In-Place Processing

The data-processing section contains two different exercises.

**Reverse index**

`invert_data()` converts branch/account/service data into a reverse index:

```text
service tag -> sorted unique (account, branch) pairs
```

**Transaction queue**

`clean_transaction_queue()` modifies the original list rather than replacing it.

It demonstrates:

- tuple → list conversion
- removal of even IDs from sets
- descending sorting of embedded lists
- duplicate primitive removal by scanning and deleting by index
- preservation of the original top-level list identity

### 4. Transactional File Modifier

`process_file_updates()` works directly with `accounts.db`.

For records whose length changes, the program shifts the remaining file contents in chunks instead of reading the complete remainder into another string.

The module demonstrates:

- `r+` file mode
- `tell()`
- `seek()`
- in-place record replacement
- chunked forward/backward shifting
- `truncate()`
- `try / except / else / finally`
- rejected-record logging
- successful-update logging

Each run prints the number of processed and rejected records.

### 5. Account Architecture & Polymorphism

The OOP section contains:

```text
                    Account
                       │
          ┌────────────┼────────────┐
          │            │            │
      Savings       Current       Credit
```

The base `Account` class provides common account state and behavior.

The subclasses implement their own settlement rules:

- **SavingsAccount** — balance cannot fall below the required minimum.
- **CurrentAccount** — supports a private overdraft limit.
- **CreditAccount** — applies the required surcharge before checking the credit limit.

The module also demonstrates:

- inheritance
- `super()`
- class attributes
- protected attributes
- private attributes and name mangling
- custom exception hierarchy
- polymorphic processing
- batch fault isolation

A failure for one account does not stop the remaining accounts from being processed.

---

## Error handling

The project defines a small exception hierarchy:

```text
BaseSystemError
├── CorruptedRecordError
├── OutOfBoundsError
└── InsufficientBalanceError
```

This allows specific problems to be reported while still giving the program a common base exception for controlled handling.

---

## Files generated at runtime

When the file-processing demonstration runs:

### `accounts.db`

The seed account file is updated in place.

### `corrupted.log`

Invalid records are recorded with their line number and reason for rejection.

### `ledger.txt`

Successfully processed account updates are recorded with a timestamp.

Because these are execution outputs rather than source files, they are excluded from version control.

---

## Assignment coverage

| Unit | Main concepts demonstrated |
|---|---|
| **Unit 1** | Nested loops, arithmetic operations, trajectory guard, short-circuit logic, early halt |
| **Unit 2** | Manual parser, quoted delimiters, escaped quotes, closures, `nonlocal`, lambda late-binding |
| **Unit 3** | Nested comprehensions, reverse indexing, in-place queue processing, set difference, sorting, duplicate removal |
| **Unit 4** | Custom exceptions, `r+`, `tell()`, `seek()`, chunked file shifting, `truncate()`, logging |
| **Unit 5** | Encapsulation, inheritance, `super()`, private/protected state, polymorphism, fault isolation |

A more detailed requirement-by-requirement explanation is available in **[Documentation.md](Documentation.md)**.

The original assignment specification is included as **[SRS-PY3 (1).md](SRS-PY3%20(1).md)**.

---

## Design constraints

The implementation follows the assignment's restrictions rather than adding unnecessary libraries or frameworks.

In particular:

- no third-party packages
- no database engine
- no web interface
- no external services
- no `split()`/ `replace()` shortcut for the required manual parser
- no read-all/rewrite approach for the required `r+` file update
- the queue is modified in place
- account settlement is handled through the account classes themselves

The goal is to keep the implementation close to the concepts being assessed in the Python syllabus.

---

## Repository

**GitHub:** https://github.com/codebynv/ptmae-python-assignment

---

## Notes

This is an academic assignment project. The implementation and documentation are organized around the supplied PTMAE SRS and its Unit 1–5 requirements.
