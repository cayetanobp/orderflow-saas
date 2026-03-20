# Portfolio Summary

## What This Project Demonstrates

OrderFlow demonstrates a production-style modular monolith with a multi-tenant backend, a business-oriented Angular frontend, Docker-based local tooling, and validation paths that are realistic for day-to-day product work.

## Technical Decisions

- Django REST Framework with JWT authentication for explicit API boundaries
- Tenant membership enforced on the server side for every protected business endpoint
- Angular standalone components with route guards, session restore, and an auth interceptor
- Docker-first frontend tooling so the project remains usable even when Node is not installed on the host
- Local PostgreSQL and Redis stack through Docker Compose, with SQLite kept available for quick backend validation

## Implemented Product Flows

- Sign in with JWT and restore session on reload
- Switch active tenant from the application shell
- Create, edit, list, and delete customers
- Create, edit, list, and delete orders with nested line items
- Apply order status transitions with traceable history notes
- Review dashboard metrics and recent activity for the active tenant

## Validation Completed

- Django test suite for tenant scoping, customer lifecycle, order lifecycle, and transition history
- Angular typecheck inside the Dockerized Node 25 Alpine workflow
- Angular production build inside the Dockerized Node 25 Alpine workflow
- Angular unit tests inside the Dockerized Node 25 Alpine workflow using headless Chromium
