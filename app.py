"""
pr-review-demo-app — a deliberately small Flask + SQLite notes app used as
a fixture for Claude Code's PR-security-review demos.

Three branches off main introduce three different PRs:
  * feat/note-detail      adds a vulnerable /notes/<id> view (IDOR)
  * feat/search           adds a vulnerable /search route   (SQL injection)
  * feat/create-note      adds a SAFE /notes/new route       (no vuln)

main is the baseline: login, logout, and a dashboard that lists the
logged-in user's own notes.
"""

import os
import sqlite3
from pathlib import Path

from flask import (
    Flask, g, redirect, render_template, request, session, url_for, abort
)

APP_ROOT = Path(__file__).resolve().parent
DB_PATH = APP_ROOT / "app.db"

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-only-do-not-use-in-prod")


# --- database helpers --------------------------------------------------------

def get_db():
    """Per-request SQLite connection."""
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def current_user():
    """Return the row of the logged-in user, or None."""
    uid = session.get("user_id")
    if uid is None:
        return None
    return get_db().execute("SELECT * FROM users WHERE id = ?", (uid,)).fetchone()


# --- auth --------------------------------------------------------------------

@app.route("/")
def index():
    if current_user():
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        row = get_db().execute(
            "SELECT id, password FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        if row and row["password"] == password:
            session["user_id"] = row["id"]
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html", error=None)


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))


# --- dashboard ---------------------------------------------------------------

@app.route("/dashboard")
def dashboard():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    notes = get_db().execute(
        "SELECT id, title FROM notes WHERE user_id = ? ORDER BY id",
        (user["id"],),
    ).fetchall()
    return render_template("dashboard.html", user=user, notes=notes)


# --- entry point -------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)
