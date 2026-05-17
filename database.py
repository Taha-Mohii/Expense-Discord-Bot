import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DB_URL)


def init_db():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS expenses(
                id SERIAL PRIMARY KEY,
                date TEXT,
                name TEXT,
                amount REAL,
                category TEXT
            )
        """
    )
    conn.commit()
    conn.close()

def add_expense(date,name,amount,category):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (date, name, amount, category) VALUES (%s , %s , %s , %s)",
                   (date, name, amount, category))
    conn.commit()
    conn.close()


def get_all():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_today(today):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses WHERE date = %s",(today,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_month(month):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses WHERE date LIKE %s", (f"{month}%",))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_expense(name):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE LOWER(name) = LOWER(%s)", (name,))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected

init_db()