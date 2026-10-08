# Documentation - PTMAE

## Student Details
- **Name:** Nirav Vala
- **Semester:** 3
- **Division:** D
- **Enrollment Number:** 25004500210223

---

## 1. Architecture and Class Diagram

```ascii
      +-------------------------------------------+
      |               Account (Base)              |
      +-------------------------------------------+
      | + total_accounts (Class Attribute)        |
      | # _account_id (Protected)                 |
      | - __balance (Private)                     |
      +-------------------------------------------+
      | + get_balance()                           |
      | + set_balance(value)                      |
      | + process_settlement(amount) [Abstract]   |
      +-------------------------------------------+
               ^             ^              ^
               |             |              |
  +------------+             |              +------------+
  |                          |                           |
+--------------------+ +-----------------------+ +-----------------------+
| SavingsAccount     | | CurrentAccount        | | CreditAccount         |
+--------------------+ +-----------------------+ +-----------------------+
| - (inherits)       | | - __overdraft_limit   | | - __credit_limit      |
+--------------------+ +-----------------------+ +-----------------------+
| + process_settl()  | | + process_settl()     | | + process_settl()     |
+--------------------+ +-----------------------+ +-----------------------+
```

---

## 2. State and Scope Tracking Table

| Scope Concept | Variable / Attribute | Description |
|---|---|---|
| **Global** | Module-level function and class definitions | No global variable is used to pass closure state or fix lambda late binding. |
| **Nonlocal** | `audited_count` | Used by the nested `filter_func` to maintain its audit count without relying on a global variable. |
| **Late-binding** | `k=k` | In `build_lambda_filters`, each lambda binds the current loop value through its default argument. |
| **Mangled Attributes**| `__balance` | The Python interpreter mangles `__balance` to `_Account__balance`, demonstrating private attribute access restrictions. |

---

## 3. Unit 1-5 Compliance Checklist

- [x] **Unit 1:** Interactive event loop using nested `while` loops, compound interest and penalty calculation using arithmetic operators only, plus short-circuit trajectory guards with demonstrations for both halt conditions.
- [x] **Unit 2:** `parse_raw_log_line` implements stateful character tracking. No `str.split()` or `str.replace()`. `nonlocal` closure state is demonstrated, and lambda functions use the `k=k` late-binding fix.
- [x] **Unit 3:** Complex nested dictionary/list comprehensions for `invert_data`. `clean_transaction_queue` performs in-place item manipulation without binding a new list. `id(data_list)` remains consistent.
- [x] **Unit 4:** Accounts database opened in `r+` mode using `f.seek()`, `f.tell()`, and `f.truncate()`. Exceptions handled by `try-except-else-finally` logic, and `corrupted.log` is generated safely.
- [x] **Unit 5:** Inherited polymorphism implemented cleanly using `super().__init__()`. Class attributes, protected/private variables appropriately handled without explicit base-class hardcoding.

---

## 4. Implementation Explanations

1. **File Overwriting (r+):** A `pos` variable tracks the read pointer using `f.tell()`. When modifying a record that changes byte-length, the script accurately reads the trailing text, goes back to the initial pointer with `f.seek()`, overwrites the space, and removes excess chunks using `f.truncate()`.
2. **Lambdas and Closures:** Instead of relying on a class instance or global parameter for our audit filters, we encapsulate state inside `create_audit_filter` and leverage nested functions to persist a running counter.
3. **Queue Optimisation:** Manipulations inside `clean_transaction_queue` strictly iterate through object items sequentially and use commands like `sort(reverse=True)` and `del` to satisfy `O(1)` memory overhead rules regarding primary arrays.


## 5. Requirement Notes

- Compound interest and penalty fees are both demonstrated with arithmetic-only calculations.
- The trajectory guard is demonstrated separately for the balance-threshold halt and the termination-flag halt.
- Rejected file records are logged using the actual input line number.
- All project classes and functions include docstrings to support the SRS maintainability requirement.
