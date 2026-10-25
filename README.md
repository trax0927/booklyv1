# Bookly

A REST API for a book review platform. Users sign up, verify their email, and manage a shared catalogue of books, which they can review and organise with tags. Admins manage tags and moderate reviews.

Live docs: https://booklyv1.onrender.com/api/v1/docs

## Features

- **Books** – create, list, update and delete books; list the books a user has added
- **Reviews** – users review books; admins can see every review
- **Tags** – admins manage tags; users attach them to books (many-to-many)
- **Accounts** – signup, login, refresh tokens, logout and `/me`
- **Email** – verification on signup and password reset by email; unverified accounts can't log in
- **Roles** – `user` and `admin` roles checked on every protected route

## Tech stack

| Area | Technology |
|---|---|
| Web framework | FastAPI |
| Models and validation | SQLModel, Pydantic, pydantic-settings |
| Database | PostgreSQL (Supabase), via async SQLAlchemy and asyncpg |
| Migrations | Alembic (async) |
| Auth | PyJWT, Passlib, itsdangerous |
| Cache and queue | Redis |
| Background jobs | Celery |
| Email | FastAPI-Mail over SMTP |
| Testing | pytest, FastAPI TestClient |
| Hosting | Render |

## Approach

- **Layered modules.** Each feature (`auth`, `books`, `reviews`, `tags`) has its own folder with `routes.py` for the HTTP endpoints, `service.py` for the database logic, and `schemas.py` for request and response models. Routes stay thin and services hold the logic.
- **Fully async.** Requests, database queries and migrations all run on async SQLAlchemy with asyncpg. Each request gets a database session through FastAPI dependency injection.
- **Schema changes go through Alembic.** Tables are never created on startup; every change is a versioned migration, and deploys run `alembic upgrade head`.
- **JWT access and refresh tokens.** Access tokens are short-lived and refresh tokens issue new ones. On logout, the token's ID is stored in Redis as a blacklist entry that expires with the token.
- **Role-based access.** A reusable `RoleChecker` dependency is attached to routes to allow `user`, `admin` or both.
- **Signed email links.** Verification and password reset links carry time-limited tokens signed with itsdangerous, so nothing extra is stored in the database.
- **Emails sent in the background.** Endpoints hand emails to a Celery task through Redis and respond straight away, so a slow mail server never slows down the API.
- **Central error handling and middleware.** Custom exceptions map to consistent JSON error responses in `errors.py`. Middleware adds request logging, CORS and a trusted host check.
- **Configuration from the environment.** All settings and secrets are loaded by pydantic-settings from environment variables or a `.env` file (see `.env.example`).
- **Versioned API.** All routes, docs and the OpenAPI schema are served under `/api/v1`.

## Running locally

```bash
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # then fill in real values
alembic upgrade head
fastapi dev src/
```

Start the Celery worker in a second terminal so emails are sent (needs Redis running):

```bash
celery -A src.celery_tasks.c_app worker --loglevel=INFO
```

Run the tests:

```bash
pytest
```

API docs are at http://localhost:8000/api/v1/docs.
