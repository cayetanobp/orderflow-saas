# Architecture

## High-Level Design

The system will use a modular monolith architecture.

## Why Modular Monolith

A modular monolith is the right first step because it keeps deployment simple while still forcing proper boundaries between domains. It also avoids fake microservices complexity.

## Main Components

### Backend

- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery

### Frontend

- Angular
- Standalone components
- Feature-based folder structure
- Typed API services

### Infrastructure

- Docker Compose for local development
- Nginx as reverse proxy in deployment
- Local validation commands documented in repository READMEs

## Planned Backend Modules

- `accounts`: authentication, users, roles
- `tenants`: tenant model and access boundaries
- `customers`: customer records and contacts
- `orders`: order aggregate and status workflow
- `notifications`: async email or event notifications
- `audit`: audit trail for sensitive changes
- `reporting`: dashboard and metrics endpoints

## Cross-Cutting Concerns

- Input validation
- Permission checks
- Tenant scoping
- Structured logging
- Pagination, filtering, ordering
- Background jobs
- Error handling
- Testing at service, API, and integration level

## Deployment Shape

- Angular static build served behind Nginx
- Django app container
- PostgreSQL container
- Redis container
- Celery worker container