import sqlite3
import bcrypt

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
DROP TABLE IF EXISTS users
""")

cursor.execute("""
DROP TABLE IF EXISTS login_attempts
""")

cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    failed_attempts INTEGER DEFAULT 0,
    locked INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE login_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    success INTEGER NOT NULL,
    reason TEXT NOT NULL,
    ip_address TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

plain_password = "password123"
hashed_password = bcrypt.hashpw(
    plain_password.encode("utf-8"),
    bcrypt.gensalt()
)

cursor.execute("""
INSERT INTO users (username, password, failed_attempts, locked)
VALUES (?, ?, ?, ?)
""", ("admin", hashed_password, 0, 0))

conn.commit()
conn.close()

print("Database reset successfully.")
print("Username: admin")
print("Password: password123")