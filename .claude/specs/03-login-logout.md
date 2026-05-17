---
# Spec: Login and Logout

## Overview
This feature implements actual login and logout functionality for the Spendly expense tracker. Currently, the `/login` route only renders a template without processing credentials, and `/logout` is a stub returning a placeholder message. This step will add secure authentication using Flask sessions, password verification via Werkzeug, and proper session management.

## Depends on
Step 2 (Registration) must be complete, as it creates users that can now log in.

## Routes
- `POST /login` — processes login form, verifies credentials, sets user session — access level: public
- `GET /logout` — clears user session and redirects to landing page — access level: logged-in

## Database changes
No database changes required. The existing `users` table with `password_hash` column is sufficient.

## Templates
- **Create:** None
- **Modify:** 
  - `templates/login.html` — add form processing and display error/success messages
  - `templates/base.html` — add conditional login/logout links in navigation

## Files to change
- `app.py` — add login POST handler and implement logout functionality
- `templates/login.html` — add form and message display
- `templates/base.html` — add dynamic navigation links based on auth state

## Files to create
None

## New dependencies
No new dependencies. Uses existing Flask, Werkzeug, and SQLite3.

## Rules for implementation
- No SQLAlchemy or ORMs — use parameterized queries only
- 
Passwords verified with `werkzeug.security.check_password_hash`
- Use CSS variables from existing stylesheets — no hardcoded hex values
- All templates must extend `base.html`
- Use `session` to track authenticated users
- Redirect authenticated users from `/login` and `/register` to appropriate pages
- Use `url_for()` for all internal links — never hardcode URLs
- Error handling: use `flash()` for messages or pass via template context
- On logout, clear session completely and redirect to landing page

## Definition of done
A specific testable checklist. Each item must be something that can be verified by running the app:
1. User can register a new account (from Step 2)
2. User can log in with correct email and password
3. User sees appropriate error for incorrect credentials
4. Authenticated user sees "Logout" link in navigation; anonymous user sees "Login"/"Register" links
5. Clicking logout clears session and redirects to landing page
6. After login, user is redirected to a protected page (to be implemented in later steps)
7. Accessing `/login` while already logged in redirects to appropriate page
8. All database queries use parameterized statements
9. No raw string returns — all routes render templates