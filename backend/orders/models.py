from django.conf import settings
from django.db import models

from customers.models import Customer
from tenants.models import Tenant


class Order(models.Model):
	class Status(models.TextChoices):
		DRAFT = 'draft', 'Draft'
		CONFIRMED = 'confirmed', 'Confirmed'
		IN_PROGRESS = 'in_progress', 'In progress'
		AWAITING_REVIEW = 'awaiting_review', 'Awaiting review'
		COMPLETED = 'completed', 'Completed'
		DELIVERED = 'delivered', 'Delivered'
		CANCELED = 'canceled', 'Canceled'

	class Priority(models.TextChoices):
		LOW = 'low', 'Low'
		MEDIUM = 'medium', 'Medium'
		HIGH = 'high', 'High'

	tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='orders')
	customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
	code = models.CharField(max_length=50)
	title = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
	priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
	due_date = models.DateField(null=True, blank=True)
	total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_orders')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('-created_at',)
		unique_together = ('tenant', 'code')

	def __str__(self):
		return self.code


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	name = models.CharField(max_length=255)
	quantity = models.PositiveIntegerField(default=1)
	unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	notes = models.TextField(blank=True)

	class Meta:
		ordering = ('id',)


class OrderStatusHistory(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='history')
	from_status = models.CharField(max_length=20, choices=Order.Status.choices, blank=True)
	to_status = models.CharField(max_length=20, choices=Order.Status.choices)
	changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='order_status_changes')
	changed_at = models.DateTimeField(auto_now_add=True)
	note = models.TextField(blank=True)

	class Meta:
		ordering = ('-changed_at',)

# Create your models here.
