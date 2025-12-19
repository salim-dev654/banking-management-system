# app/services.py

from app.database import get_connection


def create_account():
    name = input("Customer name: ")
    initial_deposit = float(input("Initial deposit: "))

    if initial_deposit < 0:
        print("❌ Deposit cannot be negative")
        return

    db = get_connection()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO accounts (customer_name, balance) VALUES (%s, %s)",
        (name, initial_deposit)
    )

    account_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, %s, %s)",
        (account_id, "DEPOSIT", initial_deposit)
    )

    db.commit()
    db.close()

    print(f"✅ Account created | Account ID: {account_id}")


def view_accounts():
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM accounts")
    accounts = cursor.fetchall()

    print("\n--- BANK ACCOUNTS ---")
    for a in accounts:
        print(f"ID: {a[0]} | Name: {a[1]} | Balance: {a[2]}")

    db.close()


def deposit_money():
    account_id = int(input("Account ID: "))
    amount = float(input("Deposit amount: "))

    if amount <= 0:
        print("❌ Invalid amount")
        return

    db = get_connection()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE accounts SET balance = balance + %s WHERE id = %s",
        (amount, account_id)
    )

    cursor.execute(
        "INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, %s, %s)",
        (account_id, "DEPOSIT", amount)
    )

    db.commit()
    db.close()

    print("✅ Deposit successful")


def withdraw_money():
    account_id = int(input("Account ID: "))
    amount = float(input("Withdrawal amount: "))

    db = get_connection()
    cursor = db.cursor()

    cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
    account = cursor.fetchone()

    if not account:
        print("❌ Account not found")
        db.close()
        return

    if account[0] < amount:
        print("❌ Insufficient funds")
        db.close()
        return

    cursor.execute(
        "UPDATE accounts SET balance = balance - %s WHERE id = %s",
        (amount, account_id)
    )

    cursor.execute(
        "INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, %s, %s)",
        (account_id, "WITHDRAW", amount)
    )

    db.commit()
    db.close()

    print("✅ Withdrawal successful")


def transaction_history():
    account_id = int(input("Account ID: "))

    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT transaction_type, amount, transaction_date
        FROM transactions
        WHERE account_id = %s
    """, (account_id,))

    records = cursor.fetchall()

    print("\n--- TRANSACTION HISTORY ---")
    for r in records:
        print(f"Type: {r[0]} | Amount: {r[1]} | Date: {r[2]}")

    db.close()
