# PTMAE — Documentation

## Student Details

- **Name:** Nirav Vala
- **Semester:** 3
- **Division:** D
- **Enrollment Number:** 25004500210223

## 1. Architecture Flow

```text
                    +-------------------------+
                    |     run_demonstration   |
                    +------------+------------+
                                 |
       +-------------------------+--------------------------+
       |                         |                          |
       v                         v                          v
+--------------+       +----------------+         +------------------+
| Unit 1       |       | Unit 2         |         | Unit 3            |
| CLI, interest|       | Manual parser  |         | Reverse index and |
| penalty, guard|      | closures, lambdas|       | in-place queue    |
+--------------+       +----------------+         +------------------+
       |                         |                          |
       +-------------------------+--------------------------+
                                 |
                                 v
                     +-----------------------+
                     | Unit 4 file processing|
                     | accounts.db, logs     |
                     +-----------+-----------+
                                 |
                                 v
                     +-----------------------+
                     | Unit 5 account classes|
                     | polymorphic settlement|
                     +-----------------------+
                                 |
                                 v
                     +-----------------------+
                     | Interactive CLI loop |
                     | interest/penalty/guard|
                     | exit or EOF handling  |
                     +-----------------------+
```

## 2. Class Diagram

```text
                 +---------------------------+
                 |       Account (Base)      |
                 +---------------------------+
                 | total_accounts            |
                 | _account_id (protected)   |
                 | __balance (private)       |
                 +---------------------------+
                   /            |            \
                  /             |             \
     +----------------+ +----------------+ +----------------+
     | SavingsAccount | | CurrentAccount | | CreditAccount  |
     +----------------+ +----------------+ +----------------+
     | Minimum 1000   | | Private         | | 2.5% surcharge |
     |                | | overdraft limit | | Credit limit   |
     +----------------+ +----------------+ +----------------+
```

The program is contained in one Python source file. The demonstration exercises each unit, then starts the interactive command loop.

## 3. State and Scope Tracking

| Concept | Example | Purpose |
|---|---|---|
| Module scope | Functions and custom exception classes | Makes required components available to the demonstration. |
| Global state | No global variables used to pass closure state or fix late binding | The closure and lambda values are scoped locally. |
| `nonlocal` | `audited_count` inside `create_audit_filter` | Maintains a counter in each returned closure. |
| Lambda late binding | `lambda record, k=k` | Captures the current loop position as a default argument. |
| Private/mangled attribute | `__balance` / `_Account__balance` | Demonstrates name mangling for the account balance. |
| Protected attribute | `_account_id` | Makes the account ID available to subclasses and the batch processor. |
| Class attribute | `total_accounts` | Counts account instances created by the base class. |

## 4. Units 1–5 Compliance Checklist

- [x] **Unit 1 — State control and trajectory guards:** The command interface uses nested `while` loops and manually scans command characters rather than using `str.split()`. Compound interest is calculated iteratively using arithmetic operations. Penalty fees accumulate a percentage amount in a loop; the number of periods defaults to one and may be supplied as a third value. The trajectory guard uses short-circuit `or`, demonstrates threshold-based stopping, and stops before applying a transaction marked with the stop flag.
- [x] **Unit 2 — Parsing and closures:** `parse_raw_log_line` scans by index, uses slicing to check for escaped quote pairs, and handles quoted delimiters, escaped quotes, empty fields, and trailing delimiters. The closure uses `nonlocal`, and each lambda binds `k=k`.
- [x] **Unit 3 — Data processing:** `invert_data` builds the reverse index through a nested-comprehension pipeline, with sorted unique account/branch tuples. `clean_transaction_queue` mutates the original list object, converts tuples to lists, sorts lists descending, removes even integer values from set elements by set difference, and removes duplicate primitive values by scanning and deleting by index.
- [x] **Unit 4 — File handling:** `process_file_updates` uses `r+`, `tell()`, `seek()`, chunked shifting, and `truncate()` when record lengths change. If the database is absent, a starter file is created on first run; subsequent record updates use `r+`. Rejected records are appended to `corrupted.log` with their input line numbers, successful updates are recorded in `ledger.txt`, and processed/rejected counts print in `finally`.
- [x] **Unit 5 — OOP and settlement:** `Account` has private `__balance`, protected `_account_id`, class attribute `total_accounts`, and validated balance methods. Savings, Current, and Credit accounts call `super().__init__()`. Savings enforces a 1000 minimum balance, Current uses a private overdraft limit, Credit applies the 2.5% surcharge, and batch settlement handles each account failure separately. Settlement amounts are non-negative debits.

## 5. Files and Runtime

The submitted folder contains only `main.py` and `documentation.md`. During execution, the program may create `accounts.db`, `corrupted.log`, and `ledger.txt`; these are runtime files and are not required in the submission ZIP.

Run from a terminal in the folder containing `main.py`:

```text
python main.py
```

The demonstrations run first. The interactive command loop then accepts:

```text
interest <principal> <rate> <years>
penalty <amount> <rate> [periods]
guard
exit
```

For example, `interest 10000 5 2` prints `Computed Interest: 1025.00`. `penalty 10000 2` computes a one-period fee of `200.00`; `penalty 5000 2 3` computes `300.00` over three periods.

If the process is launched in an output-only runner that does not provide standard input, it detects `EOFError`, prints a terminal-run hint, and exits instead of looping indefinitely. To enter commands in VS Code, use **Terminal → New Terminal** and run `python main.py` there (rather than an output-only “Run Code” panel).

The demonstration covers two compound-interest examples, two penalty examples, parser edge cases, all custom exception subclasses, lambda positions, in-place queue identity, both trajectory-stop conditions, name mangling, balance validation, file processing, and batch settlement rejections.