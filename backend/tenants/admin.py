from django.contrib import admin

from tenants.models import Membership, Tenant


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'is_active', 'created_at')
	search_fields = ('name', 'slug')


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
	list_display = ('tenant', 'user', 'role', 'created_at')
	list_filter = ('role', 'tenant')
	search_fields = ('tenant__name', 'tenant__slug', 'user__email')

# Register your models here.
