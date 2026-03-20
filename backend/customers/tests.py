from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from customers.models import Customer
from tenants.models import Membership, Tenant


class CustomerApiTests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='owner@example.com', password='test-pass-123')
		self.tenant = Tenant.objects.create(name='Alpha Studio', slug='alpha-studio')
		self.other_tenant = Tenant.objects.create(name='Beta Works', slug='beta-works')
		Membership.objects.create(tenant=self.tenant, user=self.user, role=Membership.Role.OWNER)
		Customer.objects.create(tenant=self.tenant, full_name='Alpha Customer')
		Customer.objects.create(tenant=self.other_tenant, full_name='Beta Customer')
		self.client.force_authenticate(user=self.user)

	def test_list_returns_only_active_tenant_customers(self):
		response = self.client.get('/api/v1/customers/', HTTP_X_TENANT_SLUG='alpha-studio')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['count'], 1)
		self.assertEqual(response.data['results'][0]['full_name'], 'Alpha Customer')

	def test_list_without_membership_is_forbidden(self):
		response = self.client.get('/api/v1/customers/', HTTP_X_TENANT_SLUG='beta-works')

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_create_update_and_delete_customer(self):
		create_response = self.client.post(
			'/api/v1/customers/',
			{
				'full_name': 'New Customer',
				'email': 'new@example.com',
				'phone': '+34 600 111 222',
				'company_name': 'New Co',
				'notes': 'Priority account',
			},
			format='json',
			HTTP_X_TENANT_SLUG='alpha-studio',
		)

		self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
		customer_id = create_response.data['id']

		update_response = self.client.patch(
			f'/api/v1/customers/{customer_id}/',
			{'company_name': 'Updated Co'},
			format='json',
			HTTP_X_TENANT_SLUG='alpha-studio',
		)

		self.assertEqual(update_response.status_code, status.HTTP_200_OK)
		self.assertEqual(update_response.data['company_name'], 'Updated Co')

		delete_response = self.client.delete(
			f'/api/v1/customers/{customer_id}/',
			HTTP_X_TENANT_SLUG='alpha-studio',
		)

		self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(Customer.objects.filter(id=customer_id).exists())

# Create your tests here.
