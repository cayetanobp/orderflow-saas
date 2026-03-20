from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase


class HealthcheckApiTests(APITestCase):
	def test_healthcheck_returns_ok(self):
		response = self.client.get('/api/v1/health')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['status'], 'ok')
		self.assertEqual(response.data['services']['database'], 'ok')
