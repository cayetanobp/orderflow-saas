from django.contrib import admin

from audit.models import AuditEvent


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
	list_display = ('tenant', 'entity_type', 'entity_id', 'action', 'actor', 'created_at')
	list_filter = ('tenant', 'entity_type', 'action')
	search_fields = ('entity_type', 'action', 'actor__email')

# Register your models here.
