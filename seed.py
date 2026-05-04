"""Seed the SQLite database with two users and a handful of notes per user.

Run once before starting the app:

    python seed.py
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "app.db"

SCHEMA = """
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS notes;

CREATE TABLE users (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT    NOT NULL UNIQUE,
    password TEXT    NOT NULL
);

CREATE TABLE notes (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id  INTEGER NOT NULL REFERENCES users(id),
    title    TEXT    NOT NULL,
    body     TEXT    NOT NULL
);
"""

USERS = [
    ("alice", "alicepass"),
    ("bob",   "bobpass"),
]

NOTES = [
    # (username, title, body)
    ("alice", "Grocery list",       "milk, bread, butter"),
    ("alice", "Meeting agenda",     "Q3 planning, Tuesday 9am"),
    ("alice", "Wifi password",      "Treat as confidential."),
    ("bob",   "Reading list",       "Snow Crash, Cryptonomicon"),
    ("bob",   "API key",            "sk-test-fake-not-a-real-key"),
    ("bob",   "Off-site checklist", "passport, laptop, dongles"),
]


def main():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.executescript(SCHEMA)

    for username, password in USERS:
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                   (username, password))

    user_ids = {row["username"]: row["id"] for row in
                db.execute("SELECT id, username FROM users")}

    for username, title, body in NOTES:
        db.execute("INSERT INTO notes (user_id, title, body) VALUES (?, ?, ?)",
                   (user_ids[username], title, body))

    db.commit()
    db.close()
    print(f"Seeded {DB_PATH}")


if __name__ == "__main__":
    main()
