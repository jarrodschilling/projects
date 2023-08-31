CREATE table in database.db called "users"

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    hash TEXT NOT NULL
);

Install Requirements:
flask
werkzeug.security
sqlite3
flask_session
functools

Import Requirements:
app.py
    flask - Flask, render_template, url_for, request, session
    werkzeug.security - generate_password_hash, check_password_hash
    sqlite3
    flask_session - Session
    functions - register_errors, is_valid_password, login_errors, login_required
functions.py
    flask - render_template, session, redirect
    flask_session - Session
    functools - wraps

