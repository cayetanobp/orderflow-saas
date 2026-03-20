# Backend

This directory will contain the Django and Django REST Framework application.

Planned responsibilities:

- authentication and tenant-aware access control
- customer and order management
- status workflow and history
- notifications, audit trail, and reporting endpoints

Keep the backend as a modular monolith with clear boundaries between domains.

## Implemented Foundation

- custom user model authenticated by email
- tenant and membership scoping enforced in DRF permissions
- customer CRUD
- order CRUD with nested items and transition history
- dashboard summary endpoint
- audit event logging helpers
- demo seed command for local SQLite development

## Useful Commands

```powershell
..\.venv\Scripts\python manage.py migrate
..\.venv\Scripts\python manage.py seed_demo
..\.venv\Scripts\python manage.py test
..\.venv\Scripts\python manage.py runserver
```