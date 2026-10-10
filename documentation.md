# PTMAE Documentation

**Pure Python Transactional Micro-Banking & Audit Engine**

| Field | Value |
|---|---|
| Student | Nirav Vala |
| Semester / Division | 3 / D |
| Enrollment Number | 25004500210223 |
| Source file | `main.py` (single file, five modules) |
| Imports used | `datetime` only (allowed list: `random`, `datetime`) |

The exception hierarchy is defined near the top as a shared dependency used by Units 4 and 5; this is intentional and does not change the five-unit structure.

## How to run

```
python main.py
```

| How it is started | What happens |
|---|---|
| At a keyboard | A grouped menu opens. Every value (amounts, log lines, records, accounts) is typed by the user at run time. |
| Without a keyboard (piped or automated run) | `main.py` detects that no input is available and automatically runs the **full demonstration** followed by the **self-audit**. |

### Menu map

| Option | Unit | What the user does |
|---|---|---|
| 1 | 1 | Enter principal, rate, years, penalty fee and days late |
| 2 | 1 | Enter a balance, threshold and a transaction list (the word `STOP` acts as the flag) |
| 3 | 2 | Type any log line and see the parsed tokens |
| 4 | 2 | Create an audit filter, then feed it amounts and watch its private counter grow |
| 5 | 2 | Choose how many lambda filters and give a row of values |
| 6 | 3 | Enter `BRANCH ACCOUNT TAG1,TAG2` records and see the reverse index |
| 7 | 3 | Build a mixed queue (`t`, `l`, `s`, `i`, `w` items) and see it cleaned in place |
| 8 | 4 | Add records (even broken ones), run the `r+` update, view `accounts.db`, `corrupted.log`, `ledger.txt` |
| 9 | 5 | Create Savings, Current and Credit accounts, settle a batch, set balances, see name mangling |
| 10 | 1 | Command shell (`interest`, `penalty`, `guard`, `exit`) |
| 11 | all | Full built-in demonstration of every FR |
| 12 | 4 | Pick a custom exception, raise it, catch it through `BaseSystemError` |
| 13 | all | **Self-audit**: 27 live PASS/FAIL checks covering the SRS and Appendix B |

## Verification evidence

Menu option 13 (`run_self_audit()`) executes real tests against the program's own functions and classes instead of printing fixed text. Result of the last run:

```
RESULT: 27 / 27 checks passed
```

| Group | Checks |
|---|---|
| Unit 1 | loop present, interest 1025.00, penalty 650, guard halts on threshold, guard halts on flag |
| Unit 2 | the three parser examples (quoted delimiter, doubled quote, empty/trailing field), closure counters independent, `k=k` lambdas |
| Unit 3 | inversion output exact, queue cleaned in place with the same `id()` |
| Unit 4 | exception hierarchy, `r+` update with grow, shrink and same-length records, neighbours untouched, counts, `corrupted.log` line numbers, `ledger.txt` entries |
| Unit 5 | class counter, setter validation, name mangling, `super().__init__`, savings minimum, credit surcharge, batch isolation |
| Appendix B | only `datetime` imported, no `split` / `replace` / `max` / `min` / `sum`, docstring on every function and class |

The line `FAILED B2: overdraft limit exceeded` that appears in the output is intentional: it is the batch settlement proving that one failing account does not stop the others (FR-5.3).

## Design decisions (my own choices)

| Decision | Reason |
|---|---|
| Menu-driven, fully dynamic input | The program should be usable and testable by a person, not just a fixed script. Bad input is re-asked instead of crashing (NFR-1). |
| Chunked tail shifting in `_shift_tail()` | When a record changes length, the rest of the file must move. Growing copies from the back so nothing is overwritten; shrinking copies from the front and then calls `truncate()`. The whole file is never read into memory. |
| `create_audit_filter` also exposes `.count()` | The counter stays private (`nonlocal`), yet the user can still observe it. |
| All settlements treat a positive amount as a debit | One consistent convention across Savings, Current and Credit. |
| Self-audit writes only `audit_*.tmp` files | Verification never touches the user's real `accounts.db`, `corrupted.log` or `ledger.txt`. |
| `EOFError` handled everywhere input is read | The program ends cleanly when run without a keyboard instead of printing a traceback. |

---

## (a) ASCII Class and Architecture Diagram

### Architecture

```
                         +-----------------------+
                         |      main_menu()      |   outer while loop
                         +-----------+-----------+
                                     |
   +-----------+-----------+---------+---------+-----------+-----------+
   |           |           |                   |           |           |
+--v---+   +---v----+  +---v-----+        +----v----+  +---v-----+ +---v------+
|Unit 1|   | Unit 2 |  | Unit 3  |        | Unit 4  |  | Unit 5  | | Demo     |
|State |   | Parser |  | Inverse |        | File    |  | OOP     | | (opt 11) |
|Engine|   | Closure|  | In-place|        | r+ I/O  |  | Settle  | +----------+
+--+---+   +---+----+  +----+----+        +----+----+  +----+----+
   |           |            |                  |            |
compound_   parse_raw_   invert_data()   process_file_   Account
interest()  log_line()   clean_trans-    updates()      SavingsAccount
penalty_    create_      action_queue()  _shift_tail()  CurrentAccount
fee()       audit_filter()                    |         CreditAccount
trajectory_ build_filters()                   |         execute_batch_
guard()                                 +-----v-----+   settlement()
interactive_                            | accounts.db|
loop()                                  | corrupted. |
                                        | log        |
                                        | ledger.txt |
                                        +------------+

        All modules raise / catch the common exception hierarchy
```

### Exception hierarchy

```
Exception
   |
BaseSystemError
   |-- CorruptedRecordError
   |-- OutOfBoundsError
   |-- InsufficientBalanceError
```

### Class hierarchy

```
+-------------------------------+
| Account                       |
|-------------------------------|
| total_accounts   (class attr) |
| _account_id      (protected)  |
| __balance        (private)    |
|-------------------------------|
| get_balance()                 |
| set_balance(value)  validates |
| process_settlement(amount)    |
+---------------+---------------+
                ^
   +------------+--------------+----------------------+
   |                           |                      |
+--+-----------------+  +------+-------------+  +-----+--------------+
| SavingsAccount     |  | CurrentAccount     |  | CreditAccount      |
|--------------------|  |--------------------|  |--------------------|
|                    |  | __overdraft_limit  |  | __credit_limit     |
| process_settlement |  | process_settlement |  | process_settlement |
| min balance 1000   |  | overdraft allowed  |  | amount + 2.5 %     |
+--------------------+  +--------------------+  +--------------------+
```

---

## (b) State and Scope Tracking Table

| Name | Where defined | Kind | Purpose |
|---|---|---|---|
| `audited` | `create_audit_filter` | **nonlocal** (enclosing scope) | Counts audited records; `validate()` declares `nonlocal audited`. Every filter created gets its own independent counter. |
| `k` (default arg) | `build_filters` lambda `lambda row, k=k: ...` | local default argument | Binds the loop value at definition time, which avoids the late-binding bug. No global is used. |
| `__balance` | `Account` | private instance attribute (mangled to `_Account__balance`) | Hidden balance. Outside the class `obj.__balance` raises `AttributeError`; `obj._Account__balance` works (demonstration only). |
| `_account_id` | `Account` | protected instance attribute | Account identity, used by subclasses and the batch reporter. |
| `__overdraft_limit` | `CurrentAccount` | private (mangled `_CurrentAccount__overdraft_limit`) | Overdraft allowance. |
| `__credit_limit` | `CreditAccount` | private (mangled `_CreditAccount__credit_limit`) | Remaining credit; reduced by every successful settlement. |
| `total_accounts` | `Account` | class attribute | Incremented in `Account.__init__`; shared by all subclasses. |
| `data_list` | `clean_transaction_queue` | parameter (never rebound) | The caller's list is mutated in place; `id()` stays the same. |
| `processed`, `rejected` | `process_file_updates` | local counters | Printed in the `finally` block on every run. |
| *(no module-level mutable state)* | | | No global variables carry state into closures or lambdas. The menu keeps its accounts in a local list inside `main_menu()`. |

---

## (c) Module Compliance Checklist (Units 1-5)

### Unit 1: State Control Engine

| ID | Requirement | Status | Where |
|---|---|---|---|
| FR-1.1 | Interactive event loop with nested `while`, exits only on `exit` | Done | `interactive_loop()` (outer `while running`, inner `while line == ""`), menu option 10 |
| FR-1.2 | Compound interest and penalty with `+ - * / // % **` inside loops, no `math` | Done | `compound_interest()`, `penalty_fee()` |
| FR-1.3 | Trajectory guard, short-circuit `or`, halts on threshold or flag | Done | `trajectory_guard()` (flag tested first, then threshold) |

### Unit 2: Parser and Closures

| ID | Requirement | Status | Where |
|---|---|---|---|
| FR-2.1 / 2.1.1 | `parse_raw_log_line(line, delimiter, quote_char)`, index by index, slicing, state flag | Done | `parse_raw_log_line()` uses `i`, `line[i + 1:i + 2]`, `in_quotes` |
| FR-2.1.2 | Delimiter inside quotes is data | Done | `a,"b,c",d` gives `['a','b,c','d']` |
| FR-2.1.3 | `""` becomes one literal quote | Done | `a,"say ""hi""",d` |
| FR-2.1.4 | Empty fields and trailing delimiter | Done | `a,b,` and `a,,c` |
| FR-2.2 | `create_audit_filter` with `nonlocal` counter | Done | `create_audit_filter()`, menu option 4 |
| FR-2.3 | Lambdas in a loop with `k=k`, no globals | Done | `build_filters()`, menu option 5 |

### Unit 3: Inversion and In-place Processing

| ID | Requirement | Status | Where |
|---|---|---|---|
| FR-3.1 | One dictionary comprehension, sorted unique `(Account, Branch)` tuples | Done | `invert_data()`, menu option 6 |
| FR-3.2 | In-place queue cleaning, `id(data_list)` unchanged | Done | `clean_transaction_queue()`, menu option 7 |
| FR-3.2.1 | Tuple to list | Done | Tuple is converted to a list in place. |
| FR-3.2.2 | Remove even IDs from sets by set difference | Done | `item - evens` |
| FR-3.2.3 | Sort embedded lists descending | Done | Both pre-existing lists and lists produced from tuples are sorted descending. |
| FR-3.2.4 | Remove duplicate primitives, keep first occurrence, scan and delete by index | Done | `while` loop with `del data_list[i]` |

### Unit 4: Files and Exceptions

| ID | Requirement | Status | Where |
|---|---|---|---|
| FR-4.1 | `BaseSystemError` and three subclasses | Done | top of `main.py`, menu option 12 |
| FR-4.2 | `r+` update with `tell()`, `seek()`, `truncate()`, chunked shifting | Done | `process_file_updates()`, `_shift_tail()` (grows: copy from the back; shrinks: copy from the front, then `truncate()`) |
| FR-4.3 | `try-except-else-finally` per record | Done | `process_file_updates()` |
| FR-4.3.1 | Rejected records go to `corrupted.log` with line number | Done | `Line N: reason -> text` |
| FR-4.3.2 | Accepted updates go to `ledger.txt` | Done | timestamp via `datetime` |
| FR-4.3.3 | `finally` prints processed and rejected counts | Done | printed on every run |

### Unit 5: OOP and Polymorphism

| ID | Requirement | Status | Where |
|---|---|---|---|
| FR-5.1.1 | Private `__balance`, protected `_account_id`, class attribute `total_accounts` | Done | `Account` |
| FR-5.1.2 | Validating getter and setter, suitable exception | Done | `get_balance()`, `set_balance()` raises `CorruptedRecordError` |
| FR-5.1.3 | Name mangling demonstration | Done | menu option 9 -> 5, and demo |
| FR-5.1.4 | Subclasses use `super().__init__()`, no hardcoded base name | Done | all three subclasses |
| FR-5.2 | Overridden `process_settlement` per class | Done | Savings (min 1000), Current (overdraft), Credit (+2.5 %) |
| FR-5.3 | `execute_batch_settlement` with isolated `try-except` per account, reports success and failure counts | Done | menu option 9 -> 3 |

### Constraints (SRS section 5)

| Rule | Status |
|---|---|
| Only `random` / `datetime` imported | Only `datetime` is imported |
| No `str.split()` / `str.replace()` in the parser | Not used anywhere in `main.py` |
| No `max()` / `min()` / `sum()` | Not used |
| No global state for closures or late binding | None |
| No rebinding of in-place parameters | `data_list` is only mutated |
| No read-all / rewrite with `"w"` for the update | In-place `r+` with chunk shifting. Sample/test files are also created with append-touch plus `r+` overwrite and `truncate()`, so `"w"` mode is never used anywhere in `main.py` |
| Every file opened with `with` | Yes |
| Docstrings on every function and class | Yes |
| No unguarded settlement call in the batch loop | Every call is inside `try-except` |

### Non-functional notes

| NFR | How it is met |
|---|---|
| NFR-1 Reliability | Bad numeric input is re-asked; bad records are logged; end of input exits cleanly. |
| NFR-2 Fault isolation | One bad record or one failing account never stops the rest. |
| NFR-5 Maintainability | Each module is in a labelled section with docstrings. |
| NFR-6 Verifiability | Menu option 11 runs the full demonstration; option 13 runs the 27-check self-audit; both run automatically when no keyboard input is available. |
| NFR-7 Usability | Framed headings, a grouped menu by unit, and clear prompts and error messages. |
