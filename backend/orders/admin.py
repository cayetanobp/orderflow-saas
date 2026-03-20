from django.contrib import admin

from orders.models import Order, OrderItem, OrderStatusHistory


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 0


class OrderStatusHistoryInline(admin.TabularInline):
	model = OrderStatusHistory
	extra = 0
	readonly_fields = ('from_status', 'to_status', 'changed_by', 'changed_at', 'note')
	can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('code', 'title', 'tenant', 'status', 'priority', 'due_date', 'created_at')
	list_filter = ('tenant', 'status', 'priority')
	search_fields = ('code', 'title', 'customer__full_name')
	inlines = [OrderItemInline, OrderStatusHistoryInline]

# Register your models here.
