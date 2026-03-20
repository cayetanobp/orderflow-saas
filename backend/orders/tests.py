from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from customers.models import Customer
from orders.models import Order, OrderStatusHistory
from tenants.models import Membership, Tenant


class OrderApiTests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='manager@example.com', password='test-pass-123')
		self.tenant = Tenant.objects.create(name='Alpha Studio', slug='alpha-studio')
		Membership.objects.create(tenant=self.tenant, user=self.user, role=Membership.Role.MANAGER)
		self.customer = Customer.objects.create(tenant=self.tenant, full_name='Primary Customer')
		self.client.force_authenticate(user=self.user)

	def test_create_order_calculates_total_and_writes_initial_history(self):
		payload = {
			'customer': self.customer.id,
			'code': 'ORD-001',
			'title': 'Window vinyl',
			'description': 'Install storefront vinyl set',
			'status': Order.Status.DRAFT,
			'priority': Order.Priority.HIGH,
			'items': [
				{'name': 'Design', 'quantity': 1, 'unit_price': '50.00', 'notes': ''},
				{'name': 'Print', 'quantity': 2, 'unit_price': '25.00', 'notes': ''},
			],
		}

		response = self.client.post('/api/v1/orders/', payload, format='json', HTTP_X_TENANT_SLUG='alpha-studio')

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		order = Order.objects.get(code='ORD-001')
		self.assertEqual(order.total_amount, Decimal('100.00'))
		self.assertEqual(order.history.count(), 1)
		self.assertEqual(order.history.first().to_status, Order.Status.DRAFT)

	def test_transition_creates_history_entry(self):
		order = Order.objects.create(
			tenant=self.tenant,
			customer=self.customer,
			code='ORD-002',
			title='Store sign',
			created_by=self.user,
			status=Order.Status.CONFIRMED,
		)
		OrderStatusHistory.objects.create(
			order=order,
			from_status='',
			to_status=order.status,
			changed_by=self.user,
			note='Initial status',
		)

		response = self.client.post(
			f'/api/v1/orders/{order.id}/transition/',
			{'to_status': Order.Status.IN_PROGRESS, 'note': 'Production started'},
			format='json',
			HTTP_X_TENANT_SLUG='alpha-studio',
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		order.refresh_from_db()
		self.assertEqual(order.status, Order.Status.IN_PROGRESS)
		self.assertEqual(order.history.count(), 2)

	def test_update_order_recalculates_total_and_returns_customer_name(self):
		order = Order.objects.create(
			tenant=self.tenant,
			customer=self.customer,
			code='ORD-003',
			title='Initial title',
			created_by=self.user,
			status=Order.Status.DRAFT,
		)
		OrderStatusHistory.objects.create(
			order=order,
			from_status='',
			to_status=order.status,
			changed_by=self.user,
			note='Initial status',
		)

		response = self.client.patch(
			f'/api/v1/orders/{order.id}/',
			{
				'title': 'Updated title',
				'items': [
					{'name': 'Layout', 'quantity': 2, 'unit_price': '35.00', 'notes': ''},
					{'name': 'Print', 'quantity': 1, 'unit_price': '80.00', 'notes': ''},
				],
			},
			format='json',
			HTTP_X_TENANT_SLUG='alpha-studio',
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		order.refresh_from_db()
		self.assertEqual(order.title, 'Updated title')
		self.assertEqual(order.total_amount, Decimal('150.00'))
		self.assertEqual(response.data['customer_name'], 'Primary Customer')

	def test_transition_rejects_invalid_status_jump(self):
		order = Order.objects.create(
			tenant=self.tenant,
			customer=self.customer,
			code='ORD-004',
			title='Status jump validation',
			created_by=self.user,
			status=Order.Status.CONFIRMED,
		)
		OrderStatusHistory.objects.create(
			order=order,
			from_status='',
			to_status=order.status,
			changed_by=self.user,
			note='Initial status',
		)

		response = self.client.post(
			f'/api/v1/orders/{order.id}/transition/',
			{'to_status': Order.Status.DELIVERED, 'note': 'Skipping workflow'},
			format='json',
			HTTP_X_TENANT_SLUG='alpha-studio',
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		order.refresh_from_db()
		self.assertEqual(order.status, Order.Status.CONFIRMED)

	def test_update_rejects_invalid_status_jump(self):
		order = Order.objects.create(
			tenant=self.tenant,
			customer=self.customer,
			code='ORD-005',
			title='Update jump validation',
			created_by=self.user,
			status=Order.Status.IN_PROGRESS,
		)
		OrderStatusHistory.objects.create(
			order=order,
			from_status='',
			to_status=order.status,
			changed_by=self.user,
			note='Initial status',
		)

		response = self.client.patch(
			f'/api/v1/orders/{order.id}/',
			{'status': Order.Status.DELIVERED},
			format='json',
			HTTP_X_TENANT_SLUG='alpha-studio',
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('status', response.data)
		order.refresh_from_db()
		self.assertEqual(order.status, Order.Status.IN_PROGRESS)

# Create your tests here.
