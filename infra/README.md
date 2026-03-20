# Infrastructure

This directory will contain local development and deployment assets.

Planned responsibilities:

- Docker Compose for local development
- Nginx configuration
- environment templates
- CI and deployment-related assets

Infrastructure changes must stay aligned with the modular monolith architecture.

## Quick Web Startup

From the `infra/` directory, run:

```powershell
docker compose up --build
```

This starts PostgreSQL, Redis, backend API, Celery worker, and Angular dev server.

Web entry points:

- Frontend: http://localhost:4200
- Backend API root: http://localhost:8000/api/v1/

Useful helpers:

```powershell
docker compose ps
docker compose down
docker compose down --volumes
```

## Implemented Foundation

- `docker-compose.yml` for PostgreSQL, Redis, backend, worker, Angular development, and frontend preview
- Nginx SPA fallback configuration for the frontend container
- root `.env.example` for local container defaults

## Frontend Through Docker

Use the frontend service as the default npm and Angular toolchain:

```powershell
docker compose up frontend
docker compose run --rm frontend npm run typecheck
docker compose run --rm frontend npm test
docker compose run --rm frontend npm run build:prod
docker compose --profile preview up --build frontend-preview
```

The development container uses Node 25 on Alpine and keeps `node_modules` in a named volume.

Backend, database, Redis, and frontend development services include healthchecks so Compose can gate dependent startup more reliably.

## Delivery Baseline

The repository includes documented local validation commands for backend checks, backend tests, frontend typecheck, frontend tests, and frontend production build.

Backend containers now start through Gunicorn and run migrations plus `collectstatic` automatically during container boot.

The local `backend` service also runs `seed_demo` on startup so the documented sample credentials are immediately usable.