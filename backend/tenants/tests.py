from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from tenants.models import Membership, Tenant


class MembershipManagementTests(APITestCase):
	def setUp(self):
		self.tenant = Tenant.objects.create(name='Alpha Studio', slug='alpha-studio')
		self.owner = User.objects.create_user(email='owner@example.com', password='test-pass-123')
		self.staff = User.objects.create_user(email='staff@example.com', password='test-pass-123')
		self.target = User.objects.create_user(email='target@example.com', password='test-pass-123')

		self.owner_membership = Membership.objects.create(
			tenant=self.tenant,
			user=self.owner,
			role=Membership.Role.OWNER,
		)
		self.staff_membership = Membership.objects.create(
			tenant=self.tenant,
			user=self.staff,
			role=Membership.Role.STAFF,
		)

	def test_staff_cannot_list_or_create_or_update_memberships(self):
		self.client.force_authenticate(user=self.staff)

		list_response = self.client.get('/api/v1/tenants/members/', HTTP_X_TENANT_SLUG='alpha-studio')
		self.assertEqual(list_response.status_code, status.HTTP_403_FORBIDDEN)

		create_response = self.client.post(
			'/api/v1/tenants/members/',
			{'email': 'new.member@example.com', 'role': Membership.Role.MANAGER},
			format='json',
			HTTP_X_TENANT_SLUG='alpha-studio',
		)
		self.assertEqual(create_response.status_code, status.HTTP_403_FORBIDDEN)

		update_response = self.client.patch(
			f'/api/v1/tenants/members/{self.owner_membership.id}/',
			{'role': Membership.Role.VIEWER},
			format='json',
			HTTP_X_TENANT_SLUG='alpha-studio',
		)
		self.assertEqual(update_response.status_code, status.HTTP_403_FORBIDDEN)

	def test_owner_can_list_create_and_update_memberships(self):
		self.client.force_authenticate(user=self.owner)

		list_response = self.client.get('/api/v1/tenants/members/', HTTP_X_TENANT_SLUG='alpha-studio')
		self.assertEqual(list_response.status_code, status.HTTP_200_OK)
		self.assertEqual(list_response.data['count'], 2)

		create_response = self.client.post(
			'/api/v1/tenants/members/',
			{
				'email': self.target.email,
				'first_name': 'Target',
				'last_name': 'User',
				'role': Membership.Role.MANAGER,
			},
			format='json',
			HTTP_X_TENANT_SLUG='alpha-studio',
		)
		self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

		target_membership = Membership.objects.get(tenant=self.tenant, user=self.target)
		self.assertEqual(target_membership.role, Membership.Role.MANAGER)

		update_response = self.client.patch(
			f'/api/v1/tenants/members/{target_membership.id}/',
			{'role': Membership.Role.VIEWER},
			format='json',
			HTTP_X_TENANT_SLUG='alpha-studio',
		)
		self.assertEqual(update_response.status_code, status.HTTP_200_OK)
		target_membership.refresh_from_db()
		self.assertEqual(target_membership.role, Membership.Role.VIEWER)
