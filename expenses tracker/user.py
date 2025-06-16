import sqlite3

# Create users.db
conn = sqlite3.connect("users.db")
cur = conn.cursor()

# Create users table if it doesn't exist
cur.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT)''')

# Insert a test user (Replace 'test' and 'password' as needed)
cur.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('test', 'password'))

conn.commit()
conn.close()

print("Test user created successfully.")
