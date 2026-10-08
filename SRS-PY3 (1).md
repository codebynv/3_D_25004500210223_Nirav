## Software Requirements Specification

Pure Python Transactional Micro-Banking & Audit Engine (PTMAE)

Field

Value

PTMAE-SRS-1.0

Document ID

Course

Python Programming (Units 1-5)

Student project SRS and assignment directive

Document type

Python 3.x interpreter; built-ins plus the allowed modules in §5.1

Target environment

Issued for implementation

Status

Requirement language. "Shall" = mandatory. "Should" = recommended. "May" = optional. Every requirement has a unique ID (e.g., FR-2.1) used in the traceability matrix (Appendix A).

## 1. Introduction

## 1.1 Purpose

This SRS defines the functional, non-functional, interface, and constraint requirements for PTMAE, a CLI transactional banking engine. It is the contract between the evaluator (customer) and the student (developer), and the basis for grading.

## 1.2 Scope

PTMAE is a single-process, in-memory banking engine with persistent plain-text storage. It shall:

- process account operations through an interactive command loop; client

- parse raw, unformatted log lines with a hand-written parser;

- build reverse-indexed analytical views of service data;

- update a plain-text database in place;

- settle transactions polymorphically across account types.

PTMAE is not a networked system, has no GUI, and uses no database engine.

## 1.3 Definitions and Abbreviations

Meaning

Term

Command-line interface

cu

Nested function that captures variables from its enclosing scope

Closure

Late binding

Closure variables are looked up at call time, not definition time


In-place

Mutating the existing object so all references observe the change

Python's rewriting of __x to _ClassName_ x

Name mangling

Mapping from a value (service tag) back to the keys that hold it

Reverse index

Out-of-syllabus item

Any module, package, or method listed in §5

## 1.4 References

- \* Python Programming syllabus, Units 1-5

- \* Python 3 language reference (built-in types, exceptions, file objects)

## 1.5 Document Overview

§2 describes the product context. §3 gives the detailed requirements by module. §4 gives non-functional requirements. §5 lists constraints and prohibitions. §6 lists deliverables, §7 the evaluation rubric. Appendix A maps requirements to syllabus units and marks.

## 2. Overall Description

## 2.1 Product Perspective

PTMAE is a standalone program with five cooperating modules inside one source file (main.py).

## 2.2 Product Functions (summary)

- 1. Interactive command processing with arithmetic-only interest and penalty calculation.

- 2. Manual parsing of quoted, escaped log lines.

- 3. Stateful audit filtering with closures and lambdas.


- 4. Reverse-index construction and in-place queue normalisation.

- 5. In-place record updates in accounts.db with dual-stream logging.

- 6. Polymorphic account settlement with fault isolation.

## 2.3 User Classes

User

Operator

Evaluator Runs main.py, inspects code and documentation, applies the rubric

Description

Enters commands in the CLI loop

## 2.4 Operating Environment

Any OS with a Python 3.x interpreter. No pip packages. Files are created in the working directory.

## 2.5 Design and Implementation Constraints

See §5. Summary: only syllabus constructs from Units 1-5; imports limited to the allowed modules in §5.1; no shortcut methods.

## 2.6 Assumptions and Dependencies

- ® accounts.db is a UTF-8 text file with one record per line (format in §3.7.1).

- \* Amounts are non-negative numbers in a single currency unit.

- \* Input volumes are small enough to run interactively.

## 3. Specific Requirements

## 3.1 Module 1— State Control Engine and Trajectory Guards (Unit 1)

## ID Requirement

- FR- system shall provide an interactive event loop built with

- 1.1 nested while loops that reads and executes commands until an explicit exit command is entered.

- FR- system shall compute compound interest and penalty fees 12 usingonly + - * / // % ** inside loop constructs. The math module shall not be imported or used.

- FR- system shall provide a trajectory guard that iterates

- 13 through a transaction sequence and, using short-circuit and/or evaluation, halts immediately when the balance falls below a safety threshold or a termination flag is encountered.

## Acceptance criterion

Loop continues after valid and invalid commands; exits only on the exit command.

Result matches a hand calculation for at least two

test cases.

Demonstration shows early halt on each of the two conditions.

## 3.2 Module 2 — Native Log Parser and Closure Mechanics (Unit 2)

## ID Requirement

Acceptance criterion


FR- The system shall provide parse_raw_log_line(line,

2.1 delimiter=",", quote_char=""") returning a list of clean string

tokens.

FR- The shall work index by index, using manual iteration, index

parser

211 tracking, slicing, and state flags.

FR- The shall treat a delimiter inside a quoted field as data, not as

parser

212 a separator.

FR- The shall convert an escaped quote pair ("") inside a quoted

parser

213 field into one literal quote.

FR- The shall handle empty fields and a trailing delimiter.

parser

214

FR- The system shall provide create_audit_filter (threshold) 22 returning a nested validation function that uses nonlocal to

maintain a count of audited records in the enclosing scope.

FR- The system shall build a list of lambda functions inside a loop, each 23 filtering transactions by the k-th positional criterion, and shall avoid

late-binding errors by binding k=k as a default argument. No global variables shall be used.

## 3.3 Module 3 — Data Inversion and In-Place Processing (Unit 3)

## FR-3.1 Nested comprehension inversion. Given:

```
raw_db = {
```

See sub-requirements below.

Code review shows no prohibited calls.

Counter increases across calls and is independent for each filter created.

Lambda i tests position i, not the final loop value.

```
"BRANCH_@1": [("Acc1@1", {"DEPOSIT", "UPI"}), ("Acc1@2", {"LOAN", "UPI"})],
"BRANCH_02": [("Acc101", {"SAVINGS", "UPI"}), ("Acc103", {"CARD", "DEPOSIT"})]
}
```

the system shall produce, with a single dictionary comprehension (or one nested-comprehension pipeline), a reverse index in which:

- \* each key is a service tag;

- each value is an alphabetically sorted list of unique (Account_ID, Branch_ID) tuples.

Acceptance: "UPI" maps to [("Acclel”, "BRANCH_01")] .

("Acclel”, "BRANCH_02"), (“Accle2",

FR-3.2 In-place queue optimisation. The system shall provide clean_transaction_queue(data_list) accepting a heterogeneous list (tuples, lists, sets, integers) and modifying that same list object, with no new top-level list bound to the name data_list:

## ID Operation


- FR-3.2.1 every tuple element into a list.

- FR-3.22 Remove even-numbered transaction IDs from set element using set difference. every

- FR-3.23 Sort embedded list in descending order. every

- FR-3.24 Remove duplicate primitive values while preserving first-occurrence order.

Acceptance: id(data_list) is unchanged after the call, and the caller's list shows the cleaned content.

Clarification: "O(1) auxiliary memory" applies to the top-level queue (no copy of the list). Short-lived temporaries for a single element (e.g., the set of evens for one set difference) are allowed. Duplicate removal shall be done by scanning the list itself and deleting by index, not by building a separate collection.

## 3.4 Module 4 — Transactional File Modifier and Error Logger (Unit 4)

|   |   |   |   |   | ID Requirement |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | Acceptance criterion |   |   |   |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | FR- The system shall define BaseSystemError (Exception) and issubclass checks pass; 4.1 three subclasses: CorruptedRecordError, OutOfBoundsError, catching the base class |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | catches all three. |   |   |   |   |   |   |   |   |   |   |   |
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | InsufficientBalanceError, each deriving from BaseSystemError. |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | FR- The system shall update accounts.db in r+ mode, locating Neighbouring records are 42 records with f.tell() and f.seek(), overwriting in place byte-identical after an |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | without damaging adjacent lines, and calling f.truncate() update that lengthens or |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| FR- |   |   |   |   |   |   |   |   |   |   |   | when the payload size changes. |   |   |   |   |   |   |   |   | Record processing shall use try-except-else-finally. |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | See below. |   |   | shortens a record. |   |   |   |   |   |   |   |   |   |   |
| 43 FR- |   |   |   |   |   |   | Invalid lines and |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | errors shall be written to corrupted. log |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| 43.1 |   |   |   |   |   |   |   | with the line number. |   |   |   |   |   |   | parse |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | one entry. |   |   |   |   | Each rejected record has |   |   |   |   |   |   |   |   |
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | FR- Validated updates shall be written to ledger.txt. 432 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | Each accepted update has one entry. |   |   |   |   |   |   |   |   |
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | FR- The finally block shall report the count of processed and Counts printed on every |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
|   |   |   |   |   |   | 433 rejected records. |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | run, including failures. |   |   |   |   |   |   |   |   |   |

Design note: when an updated record is longer or shorter than the original, the remainder of the file must be shifted using seek/read/write passes in chunks, not by loading the whole file and rewriting it with ny mode.

## 3.5 Module 5 — Object-Oriented Architecture and Polymorphic Engine (Unit 5)

## FR-5.1 Encapsulated account hierarchy

## ID Requirement


- FR- Base class Account shall have private __balance, protected _account_id, and a class 5.1.1 attribute total_accounts.

FR- Account shall expose public getters and setters that validate types and raise a suitable 51.2 exception on invalid input.

FR- The demonstration shall show name mangling (e.g., accessing _Account__balance, and the 513 failure of obj.__ balance).

FR- SavingsAccount, CurrentAccount, and CreditAccount shall inherit from Account and call 5.14 super().__init__() . Base-class names shall not be hardcoded in subclass constructors.

## FR-5.2 Polymorphic settlement. Each subclass shall override process_settlement(amount) :

## Class Rule

SavingsAccount Reject the transaction if the remaining balance would fall below 1000.

CurrentAccount Allow overdraft up to a private __overdraft_limit.

CreditAccount Add a 2.5% surcharge to the amount, then deduct it against the credit limit.

Rejections shall raise InsufficientBalanceError or OutOfBoundsError (FR-4.1).

FR-5.3 Isolated batch

settle a mixed list of account objects polymorphically. Each call shall be inside its own try-except, so one failure does not stop later accounts. The function shall report the successes and failures.

processor. execute_batch_settlement(account_list, transaction_amount) shall

## 3.6 External Interface Requirements

User interface. Text CLI with a prompt, a command list, and clear error messages for invalid commands.

## File interfaces.

| File |   |   |   |   |   |   |   |   |   |   |   | Direction |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | Purpose |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| accounts.db |   |   |   |   |   |   |   |   |   |   |   |   |   | Read/write (r+) |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | Account records |   |   |   |   |   |   |   |   |   |   |   |   |
|   |   |   |   |   |   |   |   |   |   |   | Append |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | Validated updates |   |   |   |   |   |   |   |   |   |   |   |   |
| corrupted. log |   |   |   |   |   |   |   |   |   |   | Append |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | Rejected records with line numbers |   |   |   |   |   |   |   |   |   |   |

Software interfaces. None, apart from the allowed modules in §5.1 (e.g, datetime for ledger timestamps).

## 3.7 Data Requirements

3.7.1 accounts.db record format (recommended). One record per line, delimiter-separated, for example:

Acc101, SAVINGS, 5200.00

-150.00

A record is corrupted if it has the wrong field count, a non-numeric balance, or an unknown account type.


## 4. Non-Functional Requirements

| ID |   |   |   |   |   |   | Category |   |   |   |   |   |   |   |   |   |   | Requirement |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NFR- 1 |   |   |   |   |   |   | Reliability |   |   |   |   |   |   |   |   | reported. |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | The program shall not crash on bad input; errors are caught, logged, and |   |
| NFR- |   |   |   |   |   |   | Fault isolation |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | A failure in one record or one account shall not stop the remaining items. |   |
| 2 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| NFR- 3 |   |   |   |   |   | Resource handling |   |   |   |   |   |   |   | block. |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | Every file shall be opened with a with statement or closed ina finally |   |
| NFR- 4 |   |   |   |   |   |   | Portability |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | The code shall run unchanged on any Python 3.x interpreter. |   |
| NFR- |   |   |   |   |   |   |   | Maintainability |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | Each module shall be in a clearly labelled section, with docstrings on every |   |
| 5 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | function and class. |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| NFR- |   |   |   |   |   |   | Verifiability |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | main.py shall include demonstration code that exercises every FR when |   |
| 6 |   |   |   |   |   |   |   |   |   |   |   |   |   | run. |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| NFR- 7 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | Prompts and messages shall be understandable without reading the |   |
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | source. |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |

## 5. Constraints and Prohibitions

Violations incur the penalty in §7.2.

## 5.1 Module policy (default-deny)

Allowed modules: random, datetime

Every other import is forbidden, whether standard-library or third-party. This includes, but is not limited to, csv, json, re, math, os, sys, sqlite3, pandas and numpy.Both import x and from x import y count. Parsing and serialisation shall be written by hand, and financial formulas shall use the arithmetic operators only. Using an allowed module is optional.

## 5.2 Prohibited shortcuts

- ® str.split() and str.replace() inthe manual parser (FR-2.1).

- max(), min(), sum() wherever explicit loop tracking or reduction is specified.

## 5.3 Memory and scope

- \* No global variables used to pass state to closures or to fix late binding.

- \* No rebinding of the parameter to a new list in in-place operations = [...]).

## 5.4 File 1/0


- \* No read-everything / modify / rewrite with "w" where an r+ in-place update is required.

- \* No file opened without with ora finally close.

## 5.5 Object orientation

- No direct access to self.__balance from outside the class except through getters/setters or correct mangled names (for demonstration only).

- No hardcoded base-class names in subclass constructors.

- No unguarded settlement call inside the batch loop.

## 6. Deliverables

- \# Deliverable

- D1 main.py

- D2 Documentation.md or Documentation.pdf

## Content

One executable file with all modules and demonstration code

- (a) ASCII class and architecture diagram; (b) state and scope tracking table covering global, nonlocal, and mangled attributes; (c) module compliance checklist for Units 1-5

## 7. Evaluation

## 7.1 Rubric

Component

State engine and trajectory guards

and closure mechanics

Native

parser

Data inversion and in-place processing

File transaction engine and logging

OOP and polymorphic engine

Architecture and documentation

Syllabus focus

Marks

Unit 1 (loops, logic, arithmetic)

15

Unit 2 (functions, scope, slicing)

1.5

Unit 3 (comprehensions, sequences)

20

Unit 4 (file I/O r+, exceptions)

20

Unit 5 (classes, encapsulation, super)

20

Design and compliance matrix

1.0

## Total

10.0

## 7.2 Penalty rule

Each use of an out-of-syllabus module, external package, or forbidden method deducts 0.25 marks. A maximum of 4 deductions applies (up to -1.0).


## Appendix B — Student Pre-Submission Checklist

- « @ No import other than random and datetime appears in main.py

- @ Parser the three examples in FR-2.1.2 FR-2.1.4 passes

- @ id(data_list) unchanged after clean_transaction_queue

- @ Neighbouring records unchanged after an r+ update
