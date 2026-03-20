# Deployment

This document defines the baseline process to clone this repository and prepare a production deployment.

## Scope

- This repository is deployment-ready as a baseline, not a one-click production template.
- Local and deployment topology stay close through Docker Compose and shared environment variables.
- Production hardening must be applied before exposing public traffic.

## Baseline Architecture

Use the services from `infra/docker-compose.yml` as the starting point:

- PostgreSQL for persistent data
- Redis for Celery broker/result backend
- Django backend API
- Celery worker
- Angular frontend

## Clone And Configure

- Clone the repository.
- Copy `.env.example` into your platform secret store or runtime environment variables.
- Replace placeholder secrets and credentials.
- Set real values for `DJANGO_ALLOWED_HOSTS` and `DJANGO_CORS_ALLOWED_ORIGINS`.

## Database Initialization

Run migrations before first traffic:

```powershell
python manage.py migrate --noinput
```

For demo environments only:

```powershell
python manage.py seed_demo
```

Do not run demo seed in production.

## Production Readiness Checklist

Use this checklist to move from demo baseline to production deployment.

### 1. Security And Secrets

- [ ] `DJANGO_DEBUG=false` in production.
- [ ] `DJANGO_SECRET_KEY` is strong and stored outside git.
- [ ] Database and Redis credentials are unique per environment.
- [ ] CORS and allowed hosts are limited to real production domains.
- [ ] HTTPS is enforced at the edge (Nginx/load balancer).
- [ ] Database and Redis are not publicly exposed.

### 2. Environment And Configuration

- [ ] Separate runtime configuration for `dev`, `staging`, and `prod`.
- [ ] Demo-only settings are disabled in production (for example demo seed).
- [ ] Environment values are managed in secret storage, not local files.
- [ ] Container image tags are pinned for repeatable deployments.

### 3. Data And Reliability

- [ ] Automated database backups are enabled.
- [ ] Restore procedure is documented and tested.
- [ ] Migrations are run before serving traffic.
- [ ] Static asset collection and serving are verified.

### 4. Quality Gates Before Release

- [ ] Backend checks pass (`python manage.py check`).
- [ ] Backend tests pass (`python manage.py test`).
- [ ] Frontend typecheck passes.
- [ ] Frontend tests pass.
- [ ] Frontend production build passes.

### 5. Observability And Operations

- [ ] Application logs are centralized.
- [ ] Health endpoint is monitored (`/api/v1/health`).
- [ ] Error and uptime alerts are configured.
- [ ] Basic incident/rollback procedure is documented.

### 6. Tenant And Access Controls

- [ ] Tenant data isolation verified across at least two memberships.
- [ ] Permission boundaries tested for non-owner users.
- [ ] Audit trail verification included in release checks.

### 7. Final Go-Live Checks

- [ ] Frontend loads and authenticates against production backend.
- [ ] Worker processes background tasks with Redis connectivity.
- [ ] Public endpoints behave correctly behind edge proxy.
- [ ] No demo credentials or fake data are exposed to real users.

## Post-Deploy Validation

- Backend health endpoint responds at `/api/v1/health`.
- Frontend loads without console errors.
- Authentication works with production credentials.
- Tenant-scoped access works across at least two memberships.
- Worker connects to Redis and processes tasks.
- Static assets are served correctly.
