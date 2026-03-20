# Frontend

This directory will contain the Angular single-page application.

Planned responsibilities:

- authenticated business interface
- customer and order workflows
- dashboards, filters, and operational views
- typed communication with the backend API

Keep the UI dense, clear, and practical for day-to-day business work.

## Implemented Foundation

- standalone Angular shell with routed pages
- login page wired to JWT endpoint contract
- dashboard, customers, and orders operational views
- customer and order CRUD workflows with form validation and feedback states
- order line item editing and explicit status transitions from the UI
- typed services for auth, dashboard, customers, and orders
- tenant header propagation through HTTP interceptor
- Docker-based Node 25 Alpine workflow for npm and Angular commands
- route guards, session restore, and automatic JWT refresh handling
- frontend unit tests running in Docker with headless Chromium

## Local Docker Workflow

Run all frontend commands through Docker Compose from `infra/`:

```powershell
docker compose up frontend
docker compose run --rm frontend npm run typecheck
docker compose run --rm frontend npm test
docker compose run --rm frontend npm run build:prod
docker compose --profile preview up --build frontend-preview
```

Notes:

- The `frontend` service uses a Node 25 Alpine image for npm and Angular CLI.
- `frontend-preview` builds the production bundle and serves it with Nginx on port `8080`.
- `node_modules` stays inside a named Docker volume to avoid host-specific installs.
- API traffic is proxied to the backend, so the browser uses `/api/v1` instead of a hardcoded host.
- Runtime overrides can be provided through `public/runtime-config.js` when needed.
- Docker runs are configured as non-interactive, so Angular analytics questions do not block builds or checks.