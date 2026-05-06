import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
SELECT username, success, reason, ip_address, timestamp
FROM login_attempts
ORDER BY timestamp DESC
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()