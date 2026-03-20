# API Plan

## API Style

- REST API with JSON responses
- Versioned under `/api/v1`
- Token-based authentication with refresh support
- Consistent validation and error payloads

## Initial Endpoint Groups

### Auth

- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`

### Tenants

- `GET /api/v1/tenants/current`
- `GET /api/v1/tenants/members`
- `POST /api/v1/tenants/members`
- `PATCH /api/v1/tenants/members/{id}`

### Customers

- `GET /api/v1/customers`
- `POST /api/v1/customers`
- `GET /api/v1/customers/{id}`
- `PATCH /api/v1/customers/{id}`
- `DELETE /api/v1/customers/{id}`

### Orders

- `GET /api/v1/orders`
- `POST /api/v1/orders`
- `GET /api/v1/orders/{id}`
- `PATCH /api/v1/orders/{id}`
- `POST /api/v1/orders/{id}/transition`
- `GET /api/v1/orders/{id}/history`

### Dashboard

- `GET /api/v1/dashboard/summary`
- `GET /api/v1/dashboard/orders-by-status`
- `GET /api/v1/dashboard/recent-activity`

## Rules

- All list endpoints must support pagination
- Filtering and ordering must be explicit and documented
- Tenant scope must be enforced server-side, never trusted from client input
- Validation errors must be predictable and field-oriented