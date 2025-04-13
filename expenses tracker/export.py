# export.py

import sqlite3
import pandas as pd

def export_to_excel(month):
    conn = sqlite3.connect("expenses.db")
    query = "SELECT date, category, amount, note FROM expenses WHERE strftime('%m', date) = ?"
    
    df = pd.read_sql_query(query, conn, params=(month,))
    conn.close()
    
    if df.empty:
        return None
    
    file_name = f"Expense_Report_{month}.xlsx"
    df.to_excel(file_name, index=False)
    return file_name
