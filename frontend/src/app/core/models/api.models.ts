export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface MembershipSummary {
  id: number;
  role: string;
  tenant_id: number;
  tenant_name: string;
  tenant_slug: string;
}

export interface CurrentUser {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  memberships: MembershipSummary[];
}

export interface DashboardSummary {
  totals: {
    customers: number;
    orders: number;
    audit_events: number;
  };
  orders_by_status: Array<{ status: string; count: number }>;
  recent_activity: Array<{
    id: number;
    order_id: number;
    order__code: string;
    from_status: string;
    to_status: string;
    changed_at: string;
    changed_by__email: string;
  }>;
}

export interface Customer {
  id: number;
  full_name: string;
  email: string;
  phone: string;
  company_name: string;
  notes: string;
  created_at: string;
  updated_at: string;
}

export interface CustomerPayload {
  full_name: string;
  email: string;
  phone: string;
  company_name: string;
  notes: string;
}

export interface OrderItem {
  id?: number;
  name: string;
  quantity: number;
  unit_price: string;
  notes: string;
}

export interface OrderHistoryEntry {
  id: number;
  from_status: string;
  to_status: string;
  changed_by_email: string;
  changed_at: string;
  note: string;
}

export interface Order {
  id: number;
  customer: number;
  customer_name?: string;
  code: string;
  title: string;
  description: string;
  status: string;
  priority: string;
  due_date: string | null;
  total_amount: string;
  created_at: string;
  updated_at: string;
  items: OrderItem[];
  history: OrderHistoryEntry[];
}

export interface OrderPayload {
  customer: number;
  code: string;
  title: string;
  description: string;
  status: string;
  priority: string;
  due_date: string | null;
  items: OrderItem[];
}

export interface OrderTransitionPayload {
  to_status: string;
  note: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}