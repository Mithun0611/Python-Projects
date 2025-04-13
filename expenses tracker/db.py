import sqlite3

def connect():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    category TEXT,
                    amount REAL,
                    note TEXT)''')
    conn.commit()
    conn.close()

def add_expense(date, category, amount, note):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO expenses (date, category, amount, note) VALUES (?, ?, ?, ?)",
                (date, category, amount, note))
    conn.commit()
    conn.close()

def fetch_expenses_by_month(month):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses WHERE strftime('%m', date) = ?", (month,))
    rows = cur.fetchall()
    conn.close()
    return rows

def update_expense(id, date, category, amount, note):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("UPDATE expenses SET date=?, category=?, amount=?, note=? WHERE id=?",
                (date, category, amount, note, id))
    conn.commit()
    conn.close()

def delete_expense(id):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()

