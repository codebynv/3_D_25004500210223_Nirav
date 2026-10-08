"""
PTMAE: Pure Python Transactional Micro-Banking & Audit Engine
Student: Nirav Vala
Semester: 3
Division: D
Enrollment Number: 25004500210223
"""

import datetime
import random

# =====================================================================
# Module 4: Custom Exception Hierarchy (Unit 4)
# =====================================================================

class BaseSystemError(Exception):
    """Base class for all PTMAE system errors."""
    pass

class CorruptedRecordError(BaseSystemError):
    """Raised when a record has an invalid format or data type."""
    pass

class OutOfBoundsError(BaseSystemError):
    """Raised when a value exceeds allowed limits."""
    pass

class InsufficientBalanceError(BaseSystemError):
    """Raised when an account has insufficient funds for a transaction."""
    pass


# =====================================================================
# Module 1: State Control Engine and Trajectory Guards (Unit 1)
# =====================================================================

def calculate_compound_interest(principal, rate, time):
    """
    Computes compound interest using only basic arithmetic operators.
    Formula: A = P(1 + r/100)^t, Interest = A - P
    """
    amount = principal * ((1 + rate / 100) ** time)
    return amount - principal

def calculate_penalty_fee(amount, rate):
    """
    Computes a penalty fee using arithmetic operators only.
    """
    return amount * rate / 100

def trajectory_guard(transactions, initial_balance, threshold, stop_flag):
    """
    Iterates through a sequence of transactions, applying them to the balance.
    Halts early using short-circuiting if balance falls below threshold or stop_flag is hit.
    """
    balance = initial_balance
    for tx in transactions:
        # Avoid using .get() to stay true to strict dict parsing, but .get is allowed built-in.
        amount = tx.get('amount', 0)
        flag = tx.get('flag', '')
        
        balance += amount
        
        if balance < threshold or flag == stop_flag:
            break
            
    return balance

def run_interactive_loop():
    """
    Interactive command processing loop built with nested while loops.
    """
    print("\n--- PTMAE Interactive Command Loop ---")
    print("Commands: 'interest <p> <r> <t>', 'guard', 'exit'")
    
    while True:
        try:
            command_line = input("PTMAE> ")
            
            if command_line == "exit":
                print("Exiting interactive loop.")
                break
                
            parts = []
            current_word = ""
            i = 0
            cmd_len = len(command_line)
            while i < cmd_len:
                char = command_line[i]
                if char == " ":
                    if current_word:
                        parts.append(current_word)
                        current_word = ""
                else:
                    current_word += char
                i += 1
            if current_word:
                parts.append(current_word)
                
            if not parts:
                continue
                
            cmd = parts[0]
            
            if cmd == "interest":
                if len(parts) == 4:
                    p = float(parts[1])
                    r = float(parts[2])
                    t = int(parts[3])
                    val = calculate_compound_interest(p, r, t)
                    print(f"Computed Interest: {val}")
                else:
                    print("Usage: interest <principal> <rate> <time>")
            elif cmd == "guard":
                txs = [{'amount': -100}, {'amount': -200, 'flag': 'STOP'}, {'amount': -500}]
                final_bal = trajectory_guard(txs, 1000, 500, 'STOP')
                print(f"Guard halted at balance: {final_bal}")
            else:
                print("Invalid command. Try 'interest', 'guard', or 'exit'.")
                
        except BaseException as e:
            if isinstance(e, KeyboardInterrupt):
                print("\nUse 'exit' to quit.")
            else:
                print(f"Error processing command: {e}")

# =====================================================================
# Module 2: Native Log Parser and Closure Mechanics (Unit 2)
# =====================================================================

def parse_raw_log_line(line, delimiter=",", quote_char='"'):
    """
    Parses a delimited string index-by-index with state flags.
    Handles escaped quotes and delimiters inside quotes.
    """
    tokens = []
    current_token = ""
    in_quotes = False
    i = 0
    length = len(line)
    
    while i < length:
        char = line[i]
        
        if char == quote_char:
            if in_quotes and i + 1 < length and line[i+1] == quote_char:
                current_token += quote_char
                i += 1
            else:
                in_quotes = not in_quotes
        elif char == delimiter and not in_quotes:
            tokens.append(current_token)
            current_token = ""
        else:
            current_token += char
            
        i += 1
        
    tokens.append(current_token)
    return tokens

def create_audit_filter(threshold):
    """
    Returns a closure that maintains state (count) using nonlocal.
    """
    audited_count = 0
    
    def filter_func(amount):
        nonlocal audited_count
        audited_count += 1
        return amount > threshold
        
    return filter_func

def build_lambda_filters():
    """
    Builds a list of lambda functions, demonstrating late-binding fix (k=k).
    No global variables are used.
    """
    filters = []
    for k in range(3):
        filters.append(lambda record, k=k: len(record) > k and record[k] == 'VALID')
    return filters


# =====================================================================
# Module 3: Data Inversion and In-Place Processing (Unit 3)
# =====================================================================

def invert_data(raw_db):
    """
    Single nested-comprehension pipeline to invert the database.
    """
    return {
        tag: sorted(list({
            (acc, branch) 
            for branch, accounts in raw_db.items() 
            for acc, tags in accounts 
            if tag in tags
        }))
        for branch_t, accounts_t in raw_db.items()
        for acc_t, tags_t in accounts_t
        for tag in tags_t
    }

def clean_transaction_queue(data_list):
    """
    Modifies data_list in place. id(data_list) remains unchanged.
    """
    i = 0
    while i < len(data_list):
        item = data_list[i]
        item_type = type(item)
        
        if item_type == tuple:
            data_list[i] = list(item)
            i += 1
        elif item_type == set:
            evens = {x for x in item if type(x) == int and x % 2 == 0}
            data_list[i] = item - evens
            i += 1
        elif item_type == list:
            data_list[i].sort(reverse=True)
            i += 1
        elif item_type in (int, float, str, bool):
            is_dup = False
            j = 0
            while j < i:
                if data_list[j] == item and type(data_list[j]) == item_type:
                    is_dup = True
                    break
                j += 1
            
            if is_dup:
                del data_list[i]
            else:
                i += 1
        else:
            i += 1


# =====================================================================
# Module 4: Transactional File Modifier and Error Logger (Unit 4)
# =====================================================================

def process_file_updates(db_path, log_path, ledger_path):
    """
    Updates accounts.db in place (r+ mode).
    """
    processed = 0
    rejected = 0
    
    with open(log_path, 'w', encoding='utf-8') as f: pass
    with open(ledger_path, 'w', encoding='utf-8') as f: pass
    
    try:
        with open(db_path, 'r+', newline='', encoding='utf-8') as f:
            line_number = 0

            while True:
                pos = f.tell()
                line = f.readline()

                if not line:
                    break

                line_number += 1
                original_len = len(line)
                clean_line = line.strip('\n')
                
                if not clean_line:
                    continue
                
                try:
                    parts = []
                    cw = ""
                    for c in clean_line:
                        if c == ",":
                            parts.append(cw.strip())
                            cw = ""
                        else:
                            cw += c
                    parts.append(cw.strip())
                    
                    if len(parts) != 3:
                        raise CorruptedRecordError("Wrong field count.")
                    
                    acc_id = parts[0]
                    acc_type = parts[1]
                    
                    if acc_type not in ["SAVINGS", "CURRENT", "CREDIT"]:
                        raise CorruptedRecordError(f"Unknown account type: {acc_type}")
                    
                    bal_str = parts[2]
                    try:
                        balance = float(bal_str)
                    except ValueError:
                        raise CorruptedRecordError("Non-numeric balance.")
                    
                    new_balance = balance + 100.0
                    new_line = f"{acc_id}, {acc_type}, {new_balance:.2f}\n"
                    
                    new_len = len(new_line)
                    
                    if new_len != original_len:
                        diff = new_len - original_len
                        chunk_size = 4096
                        
                        f.seek(0, 2)
                        eof_pos = f.tell()
                        remainder_len = eof_pos - (pos + original_len)
                        
                        if diff > 0:
                            read_pos = eof_pos
                            while remainder_len > 0:
                                bytes_to_read = chunk_size
                                if remainder_len < chunk_size:
                                    bytes_to_read = remainder_len
                                read_pos -= bytes_to_read
                                f.seek(read_pos)
                                chunk = f.read(bytes_to_read)
                                f.seek(read_pos + diff)
                                f.write(chunk)
                                remainder_len -= bytes_to_read
                            f.seek(pos)
                            f.write(new_line)
                        else:
                            f.seek(pos)
                            f.write(new_line)
                            
                            read_pos = pos + original_len
                            write_pos = pos + new_len
                            while remainder_len > 0:
                                bytes_to_read = min(chunk_size, remainder_len)
                                f.seek(read_pos)
                                chunk = f.read(bytes_to_read)
                                f.seek(write_pos)
                                f.write(chunk)
                                read_pos += bytes_to_read
                                write_pos += bytes_to_read
                                remainder_len -= bytes_to_read
                            f.truncate()
                            
                        f.seek(pos + new_len)
                    else:
                        f.seek(pos)
                        f.write(new_line)
                    
                except CorruptedRecordError as e:
                    rejected += 1
                    with open(log_path, 'a') as log_f:
                        log_f.write(f"Line {line_number}: {str(e)} -> {clean_line}\n")
                    f.seek(pos + original_len)
                except Exception as e:
                    rejected += 1
                    with open(log_path, 'a') as log_f:
                        log_f.write(f"Line {line_number}: System Error -> {clean_line}\n")
                    f.seek(pos + original_len)
                else:
                    processed += 1
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open(ledger_path, 'a') as ledg_f:
                        ledg_f.write(f"[{timestamp}] Updated {acc_id}\n")
    finally:
        print(f"File Update Complete. Processed: {processed}, Rejected: {rejected}")

# =====================================================================
# Module 5: Object-Oriented Architecture and Polymorphic Engine (Unit 5)
# =====================================================================

class Account:
    """Base account class providing common account state and validation."""

    total_accounts = 0
    
    def __init__(self, account_id, balance):
        """Initializes an account with an ID and validated balance."""
        self._account_id = account_id
        self.__balance = self._validate_balance(balance)
        Account.total_accounts += 1
        
    def _validate_balance(self, balance):
        """Validates and normalizes an account balance."""
        if type(balance) not in (int, float):
            raise BaseSystemError("Balance must be a numeric type.")
        return float(balance)
        
    def get_balance(self):
        """Returns the current private account balance."""
        return self.__balance
        
    def set_balance(self, value):
        """Validates and updates the private account balance."""
        self.__balance = self._validate_balance(value)
        
    def process_settlement(self, amount):
        """Defines the settlement interface implemented by account subclasses."""
        raise NotImplementedError("Subclasses must implement process_settlement")

class SavingsAccount(Account):
    """Savings account that maintains a minimum balance of 1000."""

    def __init__(self, account_id, balance):
        """Initializes a savings account."""
        super().__init__(account_id, balance)
        
    def process_settlement(self, amount):
        """Applies a settlement while preserving the minimum savings balance."""
        new_bal = self.get_balance() + amount
        if new_bal < 1000:
            raise InsufficientBalanceError("Savings balance cannot fall below 1000.")
        self.set_balance(new_bal)

class CurrentAccount(Account):
    """Current account that supports a configured private overdraft limit."""

    def __init__(self, account_id, balance, overdraft_limit):
        """Initializes a current account with its overdraft limit."""
        super().__init__(account_id, balance)
        self.__overdraft_limit = overdraft_limit
        
    def process_settlement(self, amount):
        """Applies a settlement within the configured overdraft limit."""
        new_bal = self.get_balance() + amount
        if new_bal < -self.__overdraft_limit:
            raise InsufficientBalanceError("Overdraft limit exceeded.")
        self.set_balance(new_bal)

class CreditAccount(Account):
    """Credit account that applies a 2.5 percent settlement surcharge."""

    def __init__(self, account_id, balance, credit_limit):
        """Initializes a credit account with its credit limit."""
        super().__init__(account_id, balance)
        self.__credit_limit = credit_limit
        
    def process_settlement(self, amount):
        """Applies a settlement and the required 2.5 percent surcharge."""
        surcharge = amount * 0.025
        total_deduction = amount + surcharge
        new_bal = self.get_balance() - total_deduction
        if new_bal < -self.__credit_limit:
            raise OutOfBoundsError("Credit limit exceeded with surcharge.")
        self.set_balance(new_bal)

def execute_batch_settlement(account_list, transaction_amount):
    """
    Settles a mixed list of accounts polymorphically.
    Isolated batch: failures do not stop the loop.
    """
    print("\n--- Batch Settlement ---")
    success = 0
    fail = 0
    
    for acc in account_list:
        try:
            acc.process_settlement(transaction_amount)
            print(f"Settled {transaction_amount} on {acc._account_id}, New Bal: {acc.get_balance()}")
            success += 1
        except BaseSystemError as e:
            print(f"Failed {acc._account_id}: {e}")
            fail += 1
            
    print(f"Batch complete. Success: {success}, Failures: {fail}")


# =====================================================================
# Demonstration Block
# =====================================================================
def run_demonstration():
    """Runs demonstrations for all PTMAE functional requirements."""
    print("=== PTMAE Demonstration Start ===")

    print("\n1. Interest and Penalty:")
    interest = calculate_compound_interest(10000, 5, 2)
    penalty = calculate_penalty_fee(10000, 2)
    print(f" Compound Interest: {interest:.2f}")
    print(f" Penalty Fee: {penalty:.2f}")

    print("\n2. Exceptions check:")
    try:
        raise CorruptedRecordError("test")
    except BaseSystemError:
        print("Caught CorruptedRecordError as BaseSystemError successfully.")
        
    print("\n3. Parse raw log line (FR-2.1):")
    line = 'field1,"field2,with,comma","field3_""escaped""",field4,'
    tokens = parse_raw_log_line(line)
    for i, t in enumerate(tokens):
        print(f" Token {i}: {t}")
        
    print("\n4. Closure and late binding (FR-2.2, FR-2.3):")
    filt = create_audit_filter(500)
    print(f" Filt(600): {filt(600)} | Filt(400): {filt(400)}")
    
    lambdas = build_lambda_filters()
    rec = ['VALID', 'INVALID', 'VALID']
    print(f" Lambda 0 (expect True): {lambdas[0](rec)}")
    print(f" Lambda 1 (expect False): {lambdas[1](rec)}")
    
    print("\n5. Data Inversion (FR-3.1):")
    raw_db = {
        "BRANCH_01": [("Acc101", {"DEPOSIT", "UPI"}), ("Acc102", {"LOAN", "UPI"})],
        "BRANCH_02": [("Acc101", {"SAVINGS", "UPI"}), ("Acc103", {"CARD", "DEPOSIT"})]
    }
    inv = invert_data(raw_db)
    for tag, val in inv.items():
        print(f" {tag}: {val}")
        
    print("\n6. In-place Queue Optimisation (FR-3.2):")
    q = [(1,2), {1,2,3,4}, [1,3,2], "dup", "dup", 10, 10]
    orig_id = id(q)
    clean_transaction_queue(q)
    new_id = id(q)
    print(f" Cleaned Queue: {q}")
    print(f" ID unchanged? {orig_id == new_id}")
    
    print("\n7. File update (FR-4):")
    process_file_updates("accounts.db", "corrupted.log", "ledger.txt")
    
    print("\n8. OOP Polymorphism and Name Mangling (FR-5):")
    s = SavingsAccount("S1", 1500)
    c = CurrentAccount("C1", 500, 2000)
    cr = CreditAccount("CR1", 0, 1000)
    
    try:
        print(s.__balance)
    except AttributeError:
        print(" Attribute __balance is successfully hidden.")
    print(f" Mangled access: {s._Account__balance}")
    
    execute_batch_settlement([s, c], -600) 
    execute_batch_settlement([cr], 500)
    
    print("\n9. Trajectory Guard (FR-1.3):")
    threshold_txs = [{'amount': -600}, {'amount': -100}]
    threshold_balance = trajectory_guard(threshold_txs, 1000, 500, 'STOP')
    print(f" Threshold halt balance: {threshold_balance}")

    flag_txs = [
        {'amount': 100},
        {'amount': 100, 'flag': 'STOP'},
        {'amount': -1000}
    ]
    flag_balance = trajectory_guard(flag_txs, 1000, 500, 'STOP')
    print(f" Stop-flag halt balance: {flag_balance}")

    print("\n10. Interactive Loop (FR-1.1):")
    run_interactive_loop()
    
    print("=== PTMAE Demonstration End ===")

if __name__ == '__main__':
    run_demonstration()
