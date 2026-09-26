import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = "spendly.db"


# ------------------------------------------------------------------ #
# Connection helper                                                   #
# ------------------------------------------------------------------ #

def get_db():
    """Return a SQLite connection with row_factory and foreign keys on."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ------------------------------------------------------------------ #
# Schema                                                              #
# ------------------------------------------------------------------ #

def init_db():
    """Create all tables (idempotent — uses IF NOT EXISTS)."""
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            email       TEXT    NOT NULL UNIQUE,
            password    TEXT    NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            title       TEXT    NOT NULL,
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    conn.commit()
    conn.close()


# ------------------------------------------------------------------ #
# Seed data                                                           #
# ------------------------------------------------------------------ #

def seed_db():
    """Insert sample data for development (idempotent via IF NOT EXISTS)."""
    conn = get_db()

    # Only seed if the users table is empty
    existing = conn.execute("SELECT COUNT(*) AS cnt FROM users").fetchone()["cnt"]
    if existing > 0:
        conn.close()
        return

    user_id = conn.execute(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
        ("Demo User", "demo@example.com",
         generate_password_hash("password")),
    ).lastrowid

    sample_expenses = [
        (user_id, "Grocery shopping",    85.40, "Food",       "2026-09-20"),
        (user_id, "Gas station",         45.00, "Transport",  "2026-09-19"),
        (user_id, "Netflix subscription",15.99, "Entertainment", "2026-09-18"),
        (user_id, "Dinner at Italiano",  62.50, "Food",       "2026-09-17"),
        (user_id, "Phone bill",          35.00, "Utilities",  "2026-09-16"),
    ]
    conn.executemany(
        "INSERT INTO expenses (user_id, title, amount, category, date) VALUES (?, ?, ?, ?, ?)",
        sample_expenses,
    )
    conn.commit()
    conn.close()