from django.conf import settings
from django.db import models


class Tenant(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField(unique=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('name',)

	def __str__(self):
		return self.name


class Membership(models.Model):
	class Role(models.TextChoices):
		OWNER = 'owner', 'Owner'
		ADMIN = 'admin', 'Admin'
		MANAGER = 'manager', 'Manager'
		STAFF = 'staff', 'Staff'
		VIEWER = 'viewer', 'Viewer'

	tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='memberships')
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='memberships')
	role = models.CharField(max_length=20, choices=Role.choices)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('tenant', 'user')
		ordering = ('tenant__name', 'user__email')

	def __str__(self):
		return f'{self.user.email} @ {self.tenant.slug}'

# Create your models here.
