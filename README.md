# Bookly

A book review REST API, built while working through [FastAPI Beyond CRUD](https://github.com/jod35/fastapi-beyond-CRUD)
by Ssali Jonathan.

## Progress

- [x] CRUD API for books (FastAPI + SQLModel)
- [x] Async PostgreSQL via SQLAlchemy/asyncpg
- [x] Alembic migrations
- [x] User accounts with hashed passwords
- [x] JWT login, refresh and auth dependencies
- [ ] Role-based access control
- [ ] Model relationships (reviews/tags)
- [ ] Background email (FastAPI-Mail)
- [ ] Celery + Redis background jobs
- [ ] Tests + deployment

## Stack

FastAPI, SQLModel, PostgreSQL, Alembic, PyJWT, Passlib

## Setup

```bash
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # then fill in real values
alembic upgrade head
fastapi dev src/
```
