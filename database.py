import sqlite3
from pathlib import Path
from datetime import datetime, date

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "queue.db"

SERVICES = ["Fees Counter", "Library", "Office", "Stationery"]

def connect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            year TEXT NOT NULL,
            password TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token INTEGER NOT NULL,
            student_name TEXT NOT NULL,
            roll_no TEXT,
            department TEXT,
            service TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Waiting',
            joined_at TEXT NOT NULL,
            called_at TEXT,
            completed_at TEXT,
            estimated_minutes INTEGER DEFAULT 0
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            queue_id INTEGER,
            rating INTEGER,
            comment TEXT,
            created_at TEXT NOT NULL
        )
    """)
    cur.execute("INSERT OR IGNORE INTO admins(username,password) VALUES (?,?)",
                ("admin", "admin123"))
    conn.commit()
    conn.close()

def admin_login(username, password):
    conn = connect()
    row = conn.execute(
        "SELECT * FROM admins WHERE username=? AND password=?",
        (username, password)
    ).fetchone()
    conn.close()
    return row is not None

def create_student(name, roll_no, department, year, password):
    conn = connect()
    try:
        conn.execute(
            "INSERT INTO students(name,roll_no,department,year,password,created_at) VALUES(?,?,?,?,?,?)",
            (name, roll_no, department, year, password, datetime.now().isoformat())
        )
        conn.commit()
        return True, "Student account created."
    except sqlite3.IntegrityError:
        return False, "Roll number already exists."
    finally:
        conn.close()

def student_login(roll_no, password):
    conn = connect()
    row = conn.execute(
        "SELECT * FROM students WHERE roll_no=? AND password=?",
        (roll_no, password)
    ).fetchone()
    conn.close()
    return row

def next_token(service):
    conn = connect()
    row = conn.execute(
        "SELECT MAX(token) AS max_token FROM queue WHERE service=? AND DATE(joined_at)=DATE('now')",
        (service,)
    ).fetchone()
    conn.close()
    return (row["max_token"] or 0) + 1

def estimate_wait(service):
    conn = connect()
    waiting = conn.execute(
        "SELECT COUNT(*) AS c FROM queue WHERE service=? AND status='Waiting'",
        (service,)
    ).fetchone()["c"]
    conn.close()
    # Default average service time: 4 minutes.
    return waiting * 4

def generate_token(service, student_name, roll_no="", department=""):
    token = next_token(service)
    wait = estimate_wait(service)
    now = datetime.now().isoformat(timespec="seconds")
    conn = connect()
    cur = conn.execute("""
        INSERT INTO queue(
            token,student_name,roll_no,department,service,status,joined_at,estimated_minutes
        ) VALUES(?,?,?,?,?,?,?,?)
    """, (token, student_name, roll_no, department, service, "Waiting", now, wait))
    conn.commit()
    queue_id = cur.lastrowid
    conn.close()
    return token, wait, queue_id

def get_waiting(service):
    conn = connect()
    rows = conn.execute("""
        SELECT * FROM queue
        WHERE service=? AND status='Waiting'
        ORDER BY id
    """, (service,)).fetchall()
    conn.close()
    return rows

def current_token(service):
    conn = connect()
    row = conn.execute("""
        SELECT * FROM queue
        WHERE service=? AND status='Serving'
        ORDER BY called_at DESC LIMIT 1
    """, (service,)).fetchone()
    conn.close()
    return row

def serve_next(service):
    conn = connect()
    old = conn.execute(
        "SELECT id FROM queue WHERE service=? AND status='Serving'",
        (service,)
    ).fetchall()
    for item in old:
        conn.execute(
            "UPDATE queue SET status='Completed', completed_at=? WHERE id=?",
            (datetime.now().isoformat(timespec="seconds"), item["id"])
        )
    row = conn.execute("""
        SELECT * FROM queue
        WHERE service=? AND status='Waiting'
        ORDER BY id LIMIT 1
    """, (service,)).fetchone()
    if not row:
        conn.commit()
        conn.close()
        return None
    conn.execute(
        "UPDATE queue SET status='Serving', called_at=? WHERE id=?",
        (datetime.now().isoformat(timespec="seconds"), row["id"])
    )
    conn.commit()
    conn.close()
    return row["token"]

def complete_current(service):
    conn = connect()
    row = conn.execute("""
        SELECT id FROM queue
        WHERE service=? AND status='Serving'
        ORDER BY called_at DESC LIMIT 1
    """, (service,)).fetchone()
    if not row:
        conn.close()
        return False
    conn.execute(
        "UPDATE queue SET status='Completed', completed_at=? WHERE id=?",
        (datetime.now().isoformat(timespec="seconds"), row["id"])
    )
    conn.commit()
    conn.close()
    return True

def cancel_queue(queue_id):
    conn = connect()
    conn.execute(
        "UPDATE queue SET status='Cancelled' WHERE id=? AND status='Waiting'",
        (queue_id,)
    )
    conn.commit()
    conn.close()

def add_feedback(queue_id, rating, comment):
    conn = connect()
    conn.execute(
        "INSERT INTO feedback(queue_id,rating,comment,created_at) VALUES(?,?,?,?)",
        (queue_id, rating, comment, datetime.now().isoformat(timespec="seconds"))
    )
    conn.commit()
    conn.close()

def get_student_active(roll_no):
    conn = connect()
    row = conn.execute("""
        SELECT * FROM queue
        WHERE roll_no=? AND status IN ('Waiting','Serving')
        ORDER BY id DESC LIMIT 1
    """, (roll_no,)).fetchone()
    conn.close()
    return row

def get_all_queue():
    conn = connect()
    rows = conn.execute("SELECT * FROM queue ORDER BY id DESC").fetchall()
    conn.close()
    return rows

def service_stats():
    conn = connect()
    rows = conn.execute("""
        SELECT service,
               COUNT(*) AS total,
               SUM(CASE WHEN status='Waiting' THEN 1 ELSE 0 END) AS waiting,
               SUM(CASE WHEN status='Serving' THEN 1 ELSE 0 END) AS serving,
               SUM(CASE WHEN status='Completed' THEN 1 ELSE 0 END) AS completed,
               SUM(CASE WHEN status='Cancelled' THEN 1 ELSE 0 END) AS cancelled
        FROM queue
        GROUP BY service
        ORDER BY total DESC
    """).fetchall()
    conn.close()
    return rows
