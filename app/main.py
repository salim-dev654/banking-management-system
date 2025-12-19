# app/main.py

from app.database import setup_database
from app.services import (
    create_account,
    view_accounts,
    deposit_money,
    withdraw_money,
    transaction_history
)


def main():
    setup_database()

    while True:
        print("""
==============================
BANKING MANAGEMENT SYSTEM
==============================
1. Create Account
2. View Accounts
3. Deposit Money
4. Withdraw Money
5. Transaction History
6. Exit
""")

        choice = input("Choose option: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            view_accounts()
        elif choice == "3":
            deposit_money()
        elif choice == "4":
            withdraw_money()
        elif choice == "5":
            transaction_history()
        elif choice == "6":
            print("👋 Exiting banking system")
            break
        else:
            print("❌ Invalid option")
