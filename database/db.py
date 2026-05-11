import os
import sqlite3

from werkzeug.security import generate_password_hash


def get_db():
    """Return a SQLite connection with row_factory and foreign keys enabled."""
    db_path = os.path.join(os.path.dirname(__file__), "..", "spendly.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables if they don't already exist."""
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )
    conn.commit()
    conn.close()


def seed_db():
    """Insert demo user and sample expenses. Safe to call multiple times."""
    conn = get_db()

    # Skip if data already exists
    cursor = conn.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    # Insert demo user
    password_hash = generate_password_hash("demo123")
    conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", password_hash),
    )

    # Get the demo user's id
    user_id = conn.execute(
        "SELECT id FROM users WHERE email = ?", ("demo@spendly.com",)
    ).fetchone()[0]

    # Insert 8 sample expenses — one per category, dates spread in current month
    expenses = [
        ("Food", 25.50, "2025-05-03", "Lunch at cafe"),
        ("Transport", 15.00, "2025-05-05", "Bus pass"),
        ("Bills", 89.99, "2025-05-07", "Electricity bill"),
        ("Health", 45.00, "2025-05-10", "Pharmacy"),
        ("Entertainment", 32.00, "2025-05-12", "Movie tickets"),
        ("Shopping", 67.80, "2025-05-15", "Groceries and toiletries"),
        ("Other", 12.99, "2025-05-18", "Stationery"),
        ("Food", 18.75, "2025-05-20", "Dinner ingredients"),
    ]
    for category, amount, date, description in expenses:
        conn.execute(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            (user_id, amount, category, date, description),
        )

    conn.commit()
    conn.close()