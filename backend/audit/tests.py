from django.test import TestCase

from accounts.models import User
from audit.models import AuditEvent
from audit.services import log_audit_event
from tenants.models import Membership, Tenant


class AuditServiceTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='owner@example.com', password='test-pass-123')
		self.tenant = Tenant.objects.create(name='Alpha Studio', slug='alpha-studio')
		Membership.objects.create(tenant=self.tenant, user=self.user, role=Membership.Role.OWNER)

	def test_log_audit_event_persists_payload(self):
		event = log_audit_event(
			tenant=self.tenant,
			actor=self.user,
			entity_type='order',
			entity_id=101,
			action='updated',
			payload={'status': 'confirmed'},
		)

		stored_event = AuditEvent.objects.get(id=event.id)
		self.assertEqual(stored_event.tenant_id, self.tenant.id)
		self.assertEqual(stored_event.actor_id, self.user.id)
		self.assertEqual(stored_event.entity_type, 'order')
		self.assertEqual(stored_event.entity_id, 101)
		self.assertEqual(stored_event.action, 'updated')
		self.assertEqual(stored_event.payload, {'status': 'confirmed'})

	def test_log_audit_event_defaults_payload_to_empty_object(self):
		event = log_audit_event(
			tenant=self.tenant,
			actor=self.user,
			entity_type='customer',
			entity_id=8,
			action='deleted',
		)

		stored_event = AuditEvent.objects.get(id=event.id)
		self.assertEqual(stored_event.payload, {})
