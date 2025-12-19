
# app/database.py

import mysql.connector
from config.config import DB_CONFIG


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def setup_database():
    db = mysql.connector.connect(
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        unix_socket=DB_CONFIG["unix_socket"]
    )
    cursor = db.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS banking_db")
    cursor.execute("USE banking_db")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        customer_name VARCHAR(100),
        balance DECIMAL(12,2) DEFAULT 0.00
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        account_id INT,
        transaction_type VARCHAR(20),
        amount DECIMAL(12,2),
        transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (account_id) REFERENCES accounts(id)
    )
    """)

    db.commit()
    db.close()
