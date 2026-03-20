# Frontend Plan

## SPA Scope

Angular frontend focused on internal business workflow, not marketing pages.

## Main Screens

- Login
- Dashboard
- Customers list
- Customer detail
- Orders list
- Order detail
- Create or edit order
- Tenant members and roles
- Activity log

## Frontend Architecture

- Feature-first structure
- Shared UI primitives folder
- Core folder for auth, guards, interceptors, config
- Typed models and API clients
- Reactive forms for create and edit flows

## UI Principles

- Clean, dense, business-oriented interface
- No decorative excess
- Fast filtering and search workflows
- Clear empty states and validation messages
- Responsive enough for laptop and tablet

## Planned Technical Pieces

- Auth interceptor
- Route guards
- State kept close to features unless global state is justified
- Reusable table and filter components
- Charting for dashboard metrics