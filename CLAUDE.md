# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in this repository.

## Project overview

Spendly is a lightweight personal expense tracker built with Flask and SQLite. It is a
student-style project where routes are implemented incrementally in numbered steps
(Step 1 → Step 9). Only the landing, register, login, terms, and privacy routes are
implemented; the rest are stubs.

## Commands

```bash
# Setup (venv already exists in the repo)
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run dev server — port 5001, NOT the Flask default 5000
python app.py

# Run all tests
pytest

# Run a specific test file
pytest tests/test_foo.py

# Run a specific test by name
pytest -k "test_name"

# Run tests with output visible
pytest -s
```

## Architecture

```
spendly/
├── app.py              # All routes — single file, no blueprints
├── database/
│   ├── __init__.py     # empty
│   └── db.py           # SQLite helpers (currently a stub — students write it in Step 1)
├── templates/
│   ├── base.html       # Shared layout — all templates extend this
│   └── *.html          # One template per page
├── static/
│   ├── css/
│   │   ├── style.css       # Global styles
│   │   └── landing.css     # Landing-page-only styles
│   └── js/
│       └── main.js         # Vanilla JS only (currently empty)
└── requirements.txt
```

**Where things belong:**
- New routes → `app.py` only, no blueprints
- DB logic → `database/db.py` only, never inline in routes
- New pages → new `.html` file extending `base.html`
- Page-specific styles → new `.css` file, not inline `<style>` tags

## Code style

- Python: PEP 8, snake_case for all variables and functions
- Templates: Jinja2 with `url_for()` for every internal link — never hardcode URLs
- Route functions: one responsibility only — fetch data, render template, done
- DB queries: always use parameterized queries (`?` placeholders) — never f-strings in SQL
- Error handling: use `abort()` for HTTP errors, not bare `return "error string"`

## Tech constraints

- **Flask only** — no FastAPI, no Django, no other web frameworks
- **SQLite only** — no PostgreSQL, no SQLAlchemy ORM, no external DB
- **Vanilla JS only** — no React, no jQuery, no npm packages
- **No new pip packages** — work within `requirements.txt` as-is unless explicitly told otherwise
- Python 3.10+ assumed — f-strings and `match` statements are fine
- The app runs on **port 5001**, not the Flask default 5000 — don't change this
- **FK enforcement is manual** — SQLite foreign keys are off by default; `get_db()` must run
  `PRAGMA foreign_keys = ON` on every connection

## Implemented vs stub routes

| Route | Status |
|---|---|
| `GET /` | Implemented — renders `landing.html` |
| `GET /register` | Implemented — renders `register.html` |
| `GET /login` | Implemented — renders `login.html` |
| `GET /terms` | Implemented — renders `terms.html` |
| `GET /privacy` | Implemented — renders `privacy.html` |
| `GET /logout` | Stub — Step 3 |
| `GET /profile` | Stub — Step 4 |
| `GET /expenses/add` | Stub — Step 7 |
| `GET /expenses/<int:id>/edit` | Stub — Step 8 |
| `GET /expenses/<int:id>/delete` | Stub — Step 9 |

**Do not implement a stub route unless the active task explicitly targets that step.**
**Never use raw string returns for stub routes** once a step is implemented — always render a template.

## Notes

- `database/db.py` is currently empty — do not assume helpers exist until the step that implements them.
- The `login.html` and `register.html` templates contain `POST` forms (action `/login`, `/register`), but `app.py` has no POST routes yet — those are part of the upcoming steps.
- `requirements.txt`: flask==3.1.3, werkzeug==3.1.6, pytest==8.3.5, pytest-flask==1.3.0.