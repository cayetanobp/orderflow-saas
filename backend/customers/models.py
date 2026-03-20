from django.db import models

from tenants.models import Tenant


class Customer(models.Model):
	tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='customers')
	full_name = models.CharField(max_length=255)
	email = models.EmailField(blank=True)
	phone = models.CharField(max_length=50, blank=True)
	company_name = models.CharField(max_length=255, blank=True)
	notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('full_name',)

	def __str__(self):
		return self.full_name

# Create your models here.
