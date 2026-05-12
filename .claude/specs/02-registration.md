# Spec: Registration

## Overview
Implement the user registration feature so new users can create accounts.
The `/register` route currently renders a static form — this step adds
the POST handler, server-side validation, password hashing, and database
insertion. After registering, users are redirected to the login page.

This is the second step of the Spendly roadmap and establishes the
foundation for authenticated sessions (login/logout) that follow in
subsequent steps.

## Depends on
- **Step 1 — Database Setup** (`01-database-setup.md`) — `get_db()`,
  `init_db()`, and `seed_db()` must be complete. The `users` table with
  `UNIQUE` email constraint is required for duplicate detection.

## Routes

- `GET /register` — Render the registration form (already implemented,
  no change needed).
- `POST /register` — Accept form submission, validate, hash password,
  insert user, redirect to `/login`. **Access: public.**

If registration is successful, redirect to `/login` with a flash
message or query parameter (e.g. `?registered=1`).

If validation fails (empty fields, invalid email, password too short),
re-render `register.html` with an `error` variable set to a descriptive
message. The template already has `{% if error %}` support.

If the email already exists in the database, re-render with an
`error` variable: `"A user with that email already exists."`

## Database changes

No new tables or columns. The `users` table from Step 1 already has
all necessary columns (`id`, `name`, `email`, `password_hash`,
`created_at`).

Add one helper function to `database/db.py`:

### `create_user(name, email, password_hash)`
- Inserts a new row into `users` using a parameterized query.
- Returns the new user's `id` (via `cursor.lastrowid`).
- Caller is responsible for hashing the password (keeps DB logic
  separate from auth logic in the route).

## Templates

No new templates. Existing `templates/register.html` already has:
- Name, email, and password input fields
- A `POST /register` form action
- `{% if error %}` block for displaying validation errors
- CSRF is **not** required for this step (will be added in a later
  step).

## Files to change

- `app.py` — Add `request` import from Flask. Replace the `register()`
  function to handle both `GET` and `POST`. On `POST`: validate input,
  check email uniqueness via `get_db()`, hash password with
  `generate_password_hash`, call `create_user()`, redirect to `/login`.

- `database/db.py` — Add the `create_user(name, email, password_hash)`
  helper function.

## Files to create

- None.

## New dependencies

No new pip packages. Uses only:
- `flask` (already in `requirements.txt`)
- `werkzeug.security.generate_password_hash` (already in
  `requirements.txt` via `werkzeug`)
- `sqlite3`, `os` (Python standard library)

## Rules for implementation

- No ORMs (no SQLAlchemy).
- **Parameterized queries only** — never use string formatting or
  f-strings in SQL.
- Passwords must be hashed using
  `from werkzeug.security import generate_password_hash`.
- Store user ID in the Flask session after registration is complete
  (session support will be needed for login in Step 3):
  ```python
  from flask import session
  session['user_id'] = user_id
  ```
- Set a secret key on the Flask app for session support:
  ```python
  import os
  app.secret_key = os.environ.get("SECRET_KEY", "dev-only-key")
  ```
- Use `url_for()` in all redirects — never hardcode URLs.
- Use CSS variables from `style.css` — never hardcode hex values in
  templates.
- All templates must extend `base.html`.
- `database/db.py` helpers must enable `PRAGMA foreign_keys = ON`
  (already done in `get_db()`).
- Validation rules:
  - Name: non-empty string, max 100 characters.
  - Email: non-empty, must contain `@`, max 254 characters.
  - Password: minimum 8 characters.

## Definition of done

- [ ] `POST /register` accepts form data (`name`, `email`, `password`).
- [ ] Empty or missing fields return an `error` message on the form.
- [ ] Password shorter than 8 characters returns an `error` message.
- [ ] Invalid email (no `@`) returns an `error` message.
- [ ] Duplicate email returns `"A user with that email already exists."`.
- [ ] Valid registration inserts a row into `users` with a hashed
      password.
- [ ] After successful registration, the user is redirected to
      `/login`.
- [ ] The session contains `user_id` after registration.
- [ ] Database helper `create_user()` exists in `database/db.py`.
- [ ] No raw SQL strings — all queries are parameterized.
- [ ] App starts without errors and the registration form still
      renders on `GET /register`.