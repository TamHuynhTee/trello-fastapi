# trello-clone

A project created with FastAPI CLI.

## Quick Start

### Start the development server

```bash
uv run fastapi dev
```

Visit http://localhost:8000

## Authentication starter

Apply migrations with `uv run alembic upgrade head` before using the API.
Set `JWT_SECRET_KEY` in your local `.env` to a random secret (do not commit it).
Generate one with `python -c 'import secrets; print(secrets.token_hex(32))'`.

The starter provides:

- `POST /api/v1/auth/register`: JSON body; returns the public user with HTTP 201.
- `POST /api/v1/auth/login`: form-encoded username/password; returns a bearer access token.
- `GET /api/v1/users/me`: requires `Authorization: Bearer <access_token>`.

Register a user:

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"alice","password":"example-password-123","email":"alice@example.com"}'
```

Log in:

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  --data-urlencode 'username=alice' \
  --data-urlencode 'password=example-password-123'
```

Use the returned token:

```bash
curl http://localhost:8000/api/v1/users/me \
  -H 'Authorization: Bearer <access_token>'
```

Alternatively, open `http://localhost:8000/docs`, register, then use **Authorize**
with the same username/password and call `/users/me`.

Usernames are case-sensitive, trimmed, and allow 3–100 letters, digits, dots,
underscores, or hyphens. Passwords allow 8–128 characters and are not trimmed.
Email and full name are optional. Passwords are hashed with Argon2; API responses
never expose password hashes. Duplicate username/email returns 409; invalid
credentials or tokens return 401.

Schemas validate requests and define public responses; repositories query the
database; services own registration transactions; routes map service errors to
HTTP responses. `app/api/dependencies.py` provides `DbSession` and `CurrentUser`
for subsequent protected endpoints.

This starter uses expiring access tokens only. Refresh tokens, logout/revocation,
email verification, password recovery, and login rate limiting are not implemented.
Add rate limiting and HTTPS before exposing authentication publicly.

Run `uv run pytest`. Auth tests override the database dependency with temporary
in-memory SQLite and do not write to the configured PostgreSQL database.

## Continuous integration

`.github/workflows/ci.yml` runs on pull requests targeting `main`, pushes to
`main`, and manual runs from GitHub Actions. The `verify` job installs Python
3.14 and locked dependencies, checks Ruff lint/formatting, runs pytest, applies
all migrations to an empty PostgreSQL 18 service, runs `alembic check`, and builds
the Docker image. After verification on `main`, the staging job publishes to GHCR
and deploys to the VPS. PRs never deploy. See [staging setup](deploy/README.md)
for required environment secrets and one-time server configuration.

CI uses disposable database credentials and a test-only JWT key from the workflow;
no GitHub secrets or local `.env` are needed. Auth tests use SQLite, while the
migration checks use PostgreSQL. This is not yet PostgreSQL integration coverage
for all API behavior. The model-only `UP042` exception is currently commented out;
enable it to retain the existing `str, Enum` convention, or migrate the enums to
`StrEnum` after reviewing behavior changes, before expecting lint to pass.

Before pushing, run:

```bash
uv sync --locked
uv run ruff check .
uv run ruff format --check .
uv run pytest -q
docker build -t trello-api:local .
```

The Docker build requires Docker Desktop or OrbStack to be running. The image
contains runtime dependencies and migrations; supply `DATABASE_URL` and
`JWT_SECRET_KEY` at runtime. Localhost inside a container refers to that container,
not your host PostgreSQL server. Environment files are excluded from the build.

Commit the workflow, Dockerfile, `.dockerignore`, config and related application
changes, push a feature branch, then open a PR to `main`. After the first run,
select `verify` as a required status check in the GitHub ruleset/branch protection
for `main`, and require a pull request before merging. Commit migration files and
`uv.lock` when they change. Do not generate migrations in CI or production.

### Deploy to FastAPI Cloud

Sign up and log in at https://fastapicloud.com, then deploy with:

```bash
uv run fastapi deploy
```

## Project Structure

- `main.py` - Your FastAPI application
- `pyproject.toml` - Project dependencies

## Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [FastAPI Cloud](https://fastapicloud.com)
