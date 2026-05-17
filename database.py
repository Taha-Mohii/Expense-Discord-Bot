import sqlite3


def init_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (date, name, amount, category) VALUES (?, ?, ?, ?)",
                   (date, name, amount, category))
    conn.commit()
    conn.close()


def get_all():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_today(today):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses WHERE date = ?",(today,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_month(month):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses WHERE date LIKE ?", (f"{month}%",))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_expense(name):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE LOWER(name) = LOWER(?)", (name,))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected

init_db()