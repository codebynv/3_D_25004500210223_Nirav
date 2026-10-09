# PTMAE — Documentation

## Student Details
- **Name:** Nirav Vala
- **Semester:** 3
- **Division:** D
- **Enrollment Number:** 25004500210223

## 1. Architecture and Class Diagram

### Architecture flow

```text
+-------------------------+
| main.py entry point     |
+------------+------------+
             |
             v
+-------------------------+
| run_demonstration()     |
+------------+------------+
             |
   +---------+----------+------------------+
   |                    |                  |
   v                    v                  v
+----------------+ +----------------+ +-------------------+
| Unit 1         | | Unit 2         | | Unit 3            |
| CLI and guards | | Parser/closures| | Reverse index and|
| Interest/fees  | | Lambda filters | | in-place queue    |
+----------------+ +----------------+ +-------------------+
             |
             +----------------------+-------------------+
                                    |                   |
                                    v                   v
                     +-----------------------+ +-----------------------+
                     | Unit 4                | | Unit 5                |
                     | accounts.db (r+)      | | Account hierarchy     |
                     | corrupted.log/ledger  | | batch settlement      |
                     +-----------------------+ +-----------------------+
```

### Account class hierarchy

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
     | Minimum 1000   | | Private overdraft| | 2.5% surcharge |
     +----------------+ +----------------+ +----------------+
```

The program is organized into five functional areas: state control and trajectory guards, manual log parsing and closures, data inversion and queue processing, transactional file updates and error logging, and account classes with polymorphic settlement.

## 2. State and Scope Tracking

| Concept | Example | Purpose |
|---|---|---|
| Module scope | Functions and exception classes | Makes the required program components available to the demonstration. |
| Global state | None used to pass closure state or fix late binding | Closure state stays local to each returned filter; each lambda binds `k=k`. |
| `nonlocal` | `audited_count` inside `create_audit_filter` | Maintains a counter in the returned closure. |
| Lambda late binding | `lambda record, k=k` | Captures the current loop value as a default argument. |
| Private/mangled attribute | `__balance` / `_Account__balance` | Demonstrates name mangling for the account balance. |
| Protected attribute | `_account_id` | Keeps the account ID available to subclasses and the batch processor. |
| Class attribute | `total_accounts` | Counts account instances created by the base class. |

## 3. Units 1–5 Compliance Checklist

- [x] **Unit 1 — State control:** Nested `while` loops support the command interface. Compound interest and penalty fees use arithmetic calculations. `trajectory_guard` uses a short-circuit `or` condition and demonstrations cover both threshold and stop-flag halts.
- [x] **Unit 2 — Parsing and closures:** `parse_raw_log_line` scans characters by index, uses a one-character lookahead slice, and handles quoted delimiters, escaped quotes, an empty middle field, and trailing delimiters. The closure uses `nonlocal`; lambdas bind `k=k`.
- [x] **Unit 3 — Data processing:** `invert_data` uses a nested-comprehension pipeline. `clean_transaction_queue` modifies the supplied list in place, converts tuples, removes even integers from sets, sorts embedded lists descending, and removes duplicate primitive values by scanning the same list.
- [x] **Unit 4 — File handling:** The account database is modified in `r+` mode with `tell`, `seek`, chunked shifting, and `truncate`. If the database is absent, a starter file is created once with valid records and one intentionally malformed record so the rejection logger is demonstrated; record updates still use `r+`. The first valid record is chosen to exercise a lengthening update. Rejected records are logged with their actual input line numbers, accepted updates go to the ledger, and counts print in `finally`.
- [x] **Unit 5 — OOP:** Custom exceptions, a private balance, protected account ID, class-level account count, validation methods, `super()` constructors, Savings/Current/Credit rules, and isolated polymorphic batch settlement are implemented. The demo shows successful settlements and overdraft/credit-limit rejection cases.

## 4. File and Runtime Notes

The submission folder contains only `main.py` and this documentation file. On the first run, `main.py` creates `accounts.db` if it is missing and also produces `corrupted.log` and `ledger.txt` while demonstrating file processing. These are runtime files, not files required in the submitted folder. Run the script with Python 3:

```text
python main.py
```

The interactive command loop supports `interest <principal> <rate> <time>`, `penalty <amount> <rate>`, `guard`, and `exit`. The demonstration includes two hand-checkable compound-interest cases, a penalty calculation, parser examples for quoted delimiters, escaped quotes, and a trailing delimiter, all three custom exception subclasses, all three lambda positions, and balance-setter validation.