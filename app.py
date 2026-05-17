from flask import Flask, render_template, request, redirect, url_for, session

from database.db import get_db, init_db, seed_db, create_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-key")


# Initialize database before first request
with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # Validation
        if not name or len(name) > 100:
            return render_template("register.html", error="Name is required.")
        if not email or len(email) > 254 or "@" not in email:
            return render_template(
                "register.html",
                error="Please enter a valid email address.",
            )
        if len(password) < 8:
            return render_template("register.html", error="Password must be at least 8 characters.")

        # Check email uniqueness
        db = get_db()
        existing = db.execute(
            "SELECT id FROM users WHERE email = ?", (email,)
        ).fetchone()
        db.close()
        if existing:
            return render_template(
                "register.html",
                error="A user with that email already exists.",
            )

        # Create user
        password_hash = generate_password_hash(password)
        user_id = create_user(name, email, password_hash)

        # Log the user in via session
        session["user_id"] = user_id

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # Basic validation
        if not email or "@" not in email:
            return render_template("login.html", error="Please enter a valid email address.")
        if not password:
            return render_template("login.html", error="Password is required.")

        # Check email uniqueness
        db = get_db()
        user = db.execute(
            "SELECT id, name, email, password_hash FROM users WHERE email = ?", (email,)
        ).fetchone()
        db.close()

        if user and check_password_hash(user["password_hash"], password):
            # Set user in session
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            return redirect(url_for("landing"))
        else:
            # Invalid credentials
            return render_template("login.html", error="Invalid email or password.")

    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #


@app.route("/logout")
def logout():
    # Clear user session
    session.pop("user_id", None)
    session.pop("user_name", None)
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)

