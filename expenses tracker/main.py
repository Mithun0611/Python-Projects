# main.py

import tkinter as tk
from tkinter import messagebox
import db
from datetime import datetime
import charts
import export



# Connect DB
db.connect()

# Main Window
root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("4000x4000")



# --- Form Labels and Entries ---
tk.Label(root, text="Date (YYYY-MM-DD)").pack()
date_entry = tk.Entry(root)
date_entry.pack()

tk.Label(root, text="Category").pack()
category_entry = tk.Entry(root)
category_entry.pack()

tk.Label(root, text="Amount").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Label(root, text="Note").pack()
note_entry = tk.Entry(root)
note_entry.pack()

# --- Submit Button ---
def save_expense():
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    note = note_entry.get()
    
    try:
        datetime.strptime(date, "%Y-%m-%d")  # Validate date
        amount = float(amount)
        db.add_expense(date, category, amount, note)
        messagebox.showinfo("Success", "Expense added successfully!")
        
        # Clear entries
        date_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        note_entry.delete(0, tk.END)
        
    except ValueError:
        messagebox.showerror("Error", "Invalid data! Check date and amount.")

tk.Button(root, text="Add Expense", command=save_expense).pack(pady=10)

# --- View Monthly Report ---
def view_report():
    def show_data():
        month = month_entry.get()
        if len(month) == 1:
            month = "0" + month  # Ensure format like '04'
        data = db.fetch_expenses_by_month(month)
        
        listbox.delete(0, tk.END)  # Clear before inserting new
        
        if not data:
            listbox.insert(tk.END, "No data found for this month.")
        else:
            for row in data:
                listbox.insert(tk.END, f"{row[1]} | ₹{row[3]} | {row[2]} | {row[4]}")

    report_window = tk.Toplevel(root)
    report_window.title("Monthly Report")
    report_window.geometry("500x300")
    
    tk.Label(report_window, text="Enter month (e.g. 04 for April):").pack()
    month_entry = tk.Entry(report_window)
    month_entry.pack()
    
    tk.Button(report_window, text="Show Report", command=show_data).pack(pady=5)
    
    listbox = tk.Listbox(report_window, width=60)
    listbox.pack(pady=10)

tk.Button(root, text="View Monthly Report", command=view_report).pack(pady=5)

def open_pie_chart():
    def show_chart():
        month = chart_month_entry.get()
        if len(month) == 1:
            month = "0" + month
        charts.show_pie_chart(month)

    chart_win = tk.Toplevel(root)
    chart_win.title("Pie Chart Analysis")
    chart_win.geometry("300x150")
    
    tk.Label(chart_win, text="Enter Month (e.g. 04 for April):").pack(pady=5)
    chart_month_entry = tk.Entry(chart_win)
    chart_month_entry.pack(pady=5)
    
    tk.Button(chart_win, text="Show Pie Chart", command=show_chart).pack(pady=10)
tk.Button(root, text="Pie Chart Analysis", command=open_pie_chart).pack(pady=5)


def open_export_window():
    def export_now():
        month = export_month_entry.get()
        if len(month) == 1:
            month = "0" + month
        file = export.export_to_excel(month)
        if file:
            messagebox.showinfo("Exported", f"Report saved as {file}")
        else:
            messagebox.showwarning("No Data", "No data to export for this month!")

    win = tk.Toplevel(root)
    win.title("Export to Excel")
    win.geometry("300x150")

    tk.Label(win, text="Enter Month (e.g. 04 for April):").pack(pady=5)
    export_month_entry = tk.Entry(win)
    export_month_entry.pack(pady=5)

    tk.Button(win, text="Export", command=export_now).pack(pady=10)
tk.Button(root, text="Export to Excel", command=open_export_window).pack(pady=5)

def view_report():
    def show_data():
        nonlocal selected_id
        month = month_entry.get()
        if len(month) == 1:
            month = "0" + month
        data = db.fetch_expenses_by_month(month)
        listbox.delete(0, tk.END)
        id_map.clear()

        if not data:
            listbox.insert(tk.END, "No data found for this month.")
        else:
            for row in data:
                display = f"{row[0]} | {row[1]} | ₹{row[3]} | {row[2]} | {row[4]}"
                listbox.insert(tk.END, display)
                id_map[display] = row  # store entire row

    def on_select(event):
        nonlocal selected_id
        try:
            selection = listbox.get(listbox.curselection())
            row = id_map.get(selection)
            if row:
                selected_id = row[0]
                date_edit.delete(0, tk.END)
                date_edit.insert(0, row[1])
                category_edit.delete(0, tk.END)
                category_edit.insert(0, row[2])
                amount_edit.delete(0, tk.END)
                amount_edit.insert(0, row[3])
                note_edit.delete(0, tk.END)
                note_edit.insert(0, row[4])
        except:
            pass

    def edit_expense():
        if selected_id is None:
            messagebox.showwarning("Select", "Please select an item to edit.")
            return
        date = date_edit.get()
        category = category_edit.get()
        amount = amount_edit.get()
        note = note_edit.get()
        try:
            db.update_expense(selected_id, date, category, float(amount), note)
            messagebox.showinfo("Updated", "Expense updated successfully!")
            show_data()
        except:
            messagebox.showerror("Error", "Check input values!")

    def delete_expense():
        if selected_id is None:
            messagebox.showwarning("Select", "Please select an item to delete.")
            return
        db.delete_expense(selected_id)
        messagebox.showinfo("Deleted", "Expense deleted!")
        show_data()

    selected_id = None
    id_map = {}

    report_window = tk.Toplevel(root)
    report_window.title("Monthly Report")
    report_window.geometry("600x450")

    tk.Label(report_window, text="Enter month (e.g. 04 for April):").pack()
    month_entry = tk.Entry(report_window)
    month_entry.pack()

    tk.Button(report_window, text="Show Report", command=show_data).pack(pady=5)

    listbox = tk.Listbox(report_window, width=70)
    listbox.pack(pady=10)
    listbox.bind('<<ListboxSelect>>', on_select)

    # Edit Fields
    tk.Label(report_window, text="Edit Selected Expense").pack(pady=5)

    date_edit = tk.Entry(report_window)
    date_edit.pack()
    category_edit = tk.Entry(report_window)
    category_edit.pack()
    amount_edit = tk.Entry(report_window)
    amount_edit.pack()
    note_edit = tk.Entry(report_window)
    note_edit.pack()

    tk.Button(report_window, text="Update Expense", command=edit_expense).pack(pady=3)
    tk.Button(report_window, text="Delete Expense", command=delete_expense).pack(pady=3)



root.mainloop()
