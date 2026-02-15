# StatusBoard

StatusBoard is a Django 5 application for tracking user availability/status across groups.  
It supports local auth via Django Allauth, optional OpenID Connect (OIDC) SSO, and group moderation workflows.

## Features

- Custom user model (`UserManager.Person`) with auto-created profile
- User status tracking (`IN`, `OUT`, `GFTD`, `A/L`, `UNKNOWN`) with notes and lock flags
- Team/group management with group moderators
- Optional external group sync from OIDC claims
- HTMX-powered partial updates for search and group membership actions
- Nightly reset command for unlocked statuses/notes

## Tech Stack

- Python + Django 5.2
- SQLite by default (PostgreSQL supported via `DATABASE_URL`)
- Django Allauth + OpenID Connect provider
- django-tables2, django-filter, crispy-forms, django-htmx

## Quick Start

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create local environment file:

```bash
cp env.example .env
```

4. Run migrations:

```bash
python manage.py migrate
```

5. (Optional) Create an admin account:

```bash
python manage.py createsuperuser
```

6. Start development server:

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Environment Variables

Configuration is loaded from `.env` at the project root.

### Core

- `SB_SECRET_KEY` (required in production)
- `SB_DEBUG` (default: `False`)
- `SB_ALLOWED_HOSTS` (comma-separated; default: empty)
- `SB_DATA_DIR` (default: project root, used for SQLite path)
- `DATABASE_URL` (optional; if unset, uses SQLite at `${SB_DATA_DIR}/db.sqlite3`)

### OIDC (optional)

Set `SB_ENABLE_OIDC=True` to enable OIDC login.

- `SB_OIDC_PROVIDER_URL`
- `SB_OIDC_NAME`
- `SB_OIDC_CLIENT_ID`
- `SB_OIDC_CLIENT_SECRET`
- `SB_OIDC_SITE_ADMIN_ROLE` (default: `site-admins`)
- `SB_OIDC_STAFF_ROLE` (default: `staff`)
- `SB_OIDC_GROUPADM_ROLE` (default: `status-admins`)


## Default Seed Data

Migrations create the default statuses:

- `UNKNOWN`
- `IN`
- `OUT`
- `GFTD` (Gone for the Day)
- `A/L` (Away on Leave [PTO] )

Migrations also create auth group `StatusApp_GroupAdmins` with `Group` model permissions.

## Useful Management Commands

- Backfill missing `UserStatus` rows for existing users:

```bash
python manage.py add_status_to_existing_users
```

- Nightly reset unlocked statuses/notes:

```bash
python manage.py nightly_reset
```

Suggested cron example:

```cron
0 5 * * * /path/to/venv/bin/python /path/to/StatusBoard/manage.py nightly_reset
```

## Deployment Notes

- WSGI entrypoint: `StatusBoard.wsgi:application`
- Example uWSGI config included at `uwsgi.ini`
- Collect static files before production deploy:

```bash
python manage.py collectstatic --noinput
```

## Project Layout

- `StatusBoard/` - Django project settings/urls
- `StatusApp/` - core status/group app
- `UserManager/` - custom user and profile models
- `menubar/` - navigation/context helpers
- `templates/`, `static/` - UI templates and assets
