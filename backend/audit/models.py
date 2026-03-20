from django.conf import settings
from django.db import models

from tenants.models import Tenant


class AuditEvent(models.Model):
	tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='audit_events')
	actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_events')
	entity_type = models.CharField(max_length=100)
	entity_id = models.PositiveIntegerField()
	action = models.CharField(max_length=100)
	payload = models.JSONField(default=dict, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-created_at',)

# Create your models here.
