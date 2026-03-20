from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from audit.models import AuditEvent
from customers.models import Customer
from orders.models import Order, OrderStatusHistory
from tenants.models import Membership, Tenant


class DashboardSummaryTests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='manager@example.com', password='test-pass-123')
		self.tenant = Tenant.objects.create(name='Alpha Studio', slug='alpha-studio')
		self.other_tenant = Tenant.objects.create(name='Beta Works', slug='beta-works')
		Membership.objects.create(tenant=self.tenant, user=self.user, role=Membership.Role.MANAGER)

		self.customer = Customer.objects.create(tenant=self.tenant, full_name='Alpha Customer')
		self.other_customer = Customer.objects.create(tenant=self.other_tenant, full_name='Beta Customer')

		self.order = Order.objects.create(
			tenant=self.tenant,
			customer=self.customer,
			code='ORD-101',
			title='Alpha order',
			status=Order.Status.CONFIRMED,
			created_by=self.user,
		)
		self.other_order = Order.objects.create(
			tenant=self.other_tenant,
			customer=self.other_customer,
			code='ORD-202',
			title='Beta order',
			status=Order.Status.DRAFT,
			created_by=self.user,
		)

		OrderStatusHistory.objects.create(
			order=self.order,
			from_status='',
			to_status=Order.Status.CONFIRMED,
			changed_by=self.user,
			note='Initial status',
		)
		OrderStatusHistory.objects.create(
			order=self.other_order,
			from_status='',
			to_status=Order.Status.DRAFT,
			changed_by=self.user,
			note='Initial status',
		)

		AuditEvent.objects.create(
			tenant=self.tenant,
			actor=self.user,
			entity_type='order',
			entity_id=self.order.id,
			action='created',
			payload={},
		)
		AuditEvent.objects.create(
			tenant=self.other_tenant,
			actor=self.user,
			entity_type='order',
			entity_id=self.other_order.id,
			action='created',
			payload={},
		)

		self.client.force_authenticate(user=self.user)

	def test_dashboard_summary_is_tenant_scoped(self):
		response = self.client.get('/api/v1/dashboard/summary', HTTP_X_TENANT_SLUG='alpha-studio')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['totals']['customers'], 1)
		self.assertEqual(response.data['totals']['orders'], 1)
		self.assertEqual(response.data['totals']['audit_events'], 1)
		self.assertEqual(len(response.data['orders_by_status']), 1)
		self.assertEqual(response.data['orders_by_status'][0]['status'], Order.Status.CONFIRMED)
		self.assertEqual(len(response.data['recent_activity']), 1)
		self.assertEqual(response.data['recent_activity'][0]['order__code'], 'ORD-101')

	def test_dashboard_summary_requires_tenant_membership(self):
		response = self.client.get('/api/v1/dashboard/summary', HTTP_X_TENANT_SLUG='beta-works')

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
