from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

MAX_FAILED_ATTEMPTS = 5


def log_login_attempt(cursor, username, success, reason, ip_address):
    cursor.execute("""
    INSERT INTO login_attempts (username, success, reason, ip_address)
    VALUES (?, ?, ?, ?)
    """, (username, success, reason, ip_address))


@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        ip_address = request.remote_addr

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user is None:
            log_login_attempt(cursor, username, 0, "Unknown username", ip_address)
            conn.commit()
            conn.close()
            error = "Invalid username or password"
            return render_template("login.html", error=error)

        user_id = user[0]
        stored_password = user[2]
        failed_attempts = user[3]
        locked = user[4]

        if locked == 1:
            log_login_attempt(cursor, username, 0, "Account locked", ip_address)
            conn.commit()
            conn.close()
            error = "Account locked due to too many failed login attempts."
            return render_template("login.html", error=error)

        if isinstance(stored_password, str):
            stored_password = stored_password.encode("utf-8")

        if bcrypt.checkpw(password.encode("utf-8"), stored_password):
            cursor.execute("""
            UPDATE users
            SET failed_attempts = 0
            WHERE id = ?
            """, (user_id,))

            log_login_attempt(cursor, username, 1, "Successful login", ip_address)

            conn.commit()
            conn.close()

            session["username"] = username
            return redirect(url_for("dashboard"))

        failed_attempts += 1

        if failed_attempts >= MAX_FAILED_ATTEMPTS:
            cursor.execute("""
            UPDATE users
            SET failed_attempts = ?, locked = 1
            WHERE id = ?
            """, (failed_attempts, user_id))

            log_login_attempt(cursor, username, 0, "Account locked after failed login", ip_address)
            error = "Account locked due to too many failed login attempts."
        else:
            cursor.execute("""
            UPDATE users
            SET failed_attempts = ?
            WHERE id = ?
            """, (failed_attempts, user_id))

            log_login_attempt(cursor, username, 0, "Invalid password", ip_address)
            error = f"Invalid username or password. Attempts left: {MAX_FAILED_ATTEMPTS - failed_attempts}"

        conn.commit()
        conn.close()

    return render_template("login.html", error=error)


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", username=session["username"])


@app.route("/logs")
def logs():
    if "username" not in session:
        return redirect(url_for("login"))

    if session["username"] != "admin":
        return "Unauthorized", 403

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT username, success, reason, ip_address, timestamp
    FROM login_attempts
    ORDER BY timestamp DESC
    """)

    logs = cursor.fetchall()
    conn.close()

    failed_count = sum(1 for log in logs if log[1] == 0)
    brute_force_detected = failed_count >= 5

    return render_template(
        "logs.html",
        logs=logs,
        failed_count=failed_count,
        brute_force_detected=brute_force_detected
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)