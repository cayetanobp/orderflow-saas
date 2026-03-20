from django.contrib import admin

from customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = ('full_name', 'company_name', 'email', 'tenant', 'created_at')
	search_fields = ('full_name', 'company_name', 'email')
	list_filter = ('tenant',)

# Register your models here.
