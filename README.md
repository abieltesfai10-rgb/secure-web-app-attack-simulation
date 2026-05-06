Project Overview

This application was built to demonstrate core Application Security (AppSec) principles:

Identify and exploit a vulnerability (SQL Injection)
Remediate the vulnerability using secure coding practices
Implement authentication security controls
Add detection mechanisms (SIEM-style logging and alerting)
⚠️ Vulnerability Demonstrated
SQL Injection (Authentication Bypass)

The initial version of the application used unsafe string-based SQL queries:

SELECT * FROM users WHERE username = 'input' AND password = 'input'

This allowed authentication bypass using payloads such as:

admin' OR '1'='1' --
🔧 Security Fixes Implemented
✅ Parameterized Queries

Prevented SQL injection by ensuring user input is treated strictly as data.

🔐 Password Hashing (bcrypt)
Eliminated plaintext password storage
Implemented secure password verification
🔑 Session-Based Authentication
Secure login session handling
Protected routes (dashboard access control)
Logout functionality
🚫 Account Lockout
Locks account after 5 failed login attempts
Prevents brute-force attacks
📊 Detection & Monitoring (SIEM-Style)
📝 Login Attempt Logging

All authentication events are logged with:

Username
Success / Failure
Failure reason
IP address
Timestamp
🚨 Brute-Force Detection
Counts failed login attempts
Triggers alert when threshold is exceeded
⚠️ Brute Force Activity Detected!
🔒 Admin-Only Log Access
/logs endpoint restricted to admin users
Prevents unauthorized access to sensitive security data
🧠 Skills Demonstrated
Flask Web Development
Secure Authentication Design
SQL Injection Exploitation & Remediation
Password Hashing (bcrypt)
Session Management
Access Control
Brute-Force Mitigation
Security Logging & Monitoring
Basic SIEM Detection Logic
🖥️ Tech Stack
Python
Flask
SQLite
bcrypt
📁 Project Structure
secure-web-app-attack-simulation/
│
├── app.py
├── database.py
├── users.db
├── view_logs.py
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   └── logs.html
▶️ How to Run
1. Install dependencies
pip install flask bcrypt
2. Initialize database
python database.py
3. Run application
python app.py
4. Access in browser
http://127.0.0.1:5000
🔑 Test Credentials
Username: admin
Password: password123
🧪 Testing Scenarios
✅ Valid Login
Successful authentication redirects to dashboard
❌ Invalid Login
Failed attempts tracked and displayed
🔒 Account Lockout
Account locks after 5 failed attempts
🚫 SQL Injection Attempt
admin' OR '1'='1' --
Properly blocked
📊 Log Monitoring
View logs at:
http://127.0.0.1:5000/logs
📌 Key Takeaway

This project demonstrates not just how vulnerabilities are exploited, but how they are prevented, monitored, and detected in a real-world application.