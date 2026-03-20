# Domain Model

## Core Entities

### Tenant

Represents one company or business account.

Fields:
- id
- name
- slug
- is_active
- created_at
- updated_at

### User

Represents a system user.

Fields:
- id
- email
- first_name
- last_name
- is_active
- created_at
- updated_at

### Membership

Links users to tenants with roles.

Fields:
- id
- tenant
- user
- role
- created_at

Roles:
- owner
- admin
- manager
- staff
- viewer

### Customer

Represents a customer inside a tenant.

Fields:
- id
- tenant
- full_name
- email
- phone
- company_name
- notes
- created_at
- updated_at

### Order

Main aggregate root for business workflow.

Fields:
- id
- tenant
- customer
- code
- title
- description
- status
- priority
- due_date
- total_amount
- created_by
- created_at
- updated_at

Statuses:
- draft
- confirmed
- in_progress
- awaiting_review
- completed
- delivered
- canceled

### OrderItem

Child line item for an order.

Fields:
- id
- order
- name
- quantity
- unit_price
- notes

### OrderStatusHistory

Stores status changes for traceability.

Fields:
- id
- order
- from_status
- to_status
- changed_by
- changed_at
- note

### AuditEvent

Captures sensitive changes.

Fields:
- id
- tenant
- actor
- entity_type
- entity_id
- action
- payload
- created_at