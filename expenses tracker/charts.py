# charts.py

import sqlite3
import matplotlib.pyplot as plt

def show_pie_chart(month):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    
    cur.execute("SELECT category, SUM(amount) FROM expenses WHERE strftime('%m', date) = ? GROUP BY category", (month,))
    data = cur.fetchall()
    conn.close()
    
    if not data:
        print("No data to show!")
        return
    
    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]
    
    # Plotting
    plt.figure(figsize=(6,6))
    plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=90)
    plt.title(f"Expenses Breakdown - Month {month}")
    plt.tight_layout()
    plt.show()
