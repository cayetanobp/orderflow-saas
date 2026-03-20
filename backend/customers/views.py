from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from audit.services import log_audit_event
from customers.models import Customer
from customers.serializers import CustomerSerializer
from tenants.permissions import HasTenantMembership


class CustomerViewSet(viewsets.ModelViewSet):
	serializer_class = CustomerSerializer
	permission_classes = [IsAuthenticated, HasTenantMembership]
	filterset_fields = ('company_name',)
	search_fields = ('full_name', 'email', 'company_name')
	ordering_fields = ('full_name', 'created_at', 'updated_at')
	ordering = ('full_name',)

	def get_queryset(self):
		return Customer.objects.filter(tenant=self.request.tenant)

	def perform_create(self, serializer):
		customer = serializer.save(tenant=self.request.tenant)
		log_audit_event(
			tenant=self.request.tenant,
			actor=self.request.user,
			entity_type='customer',
			entity_id=customer.id,
			action='created',
			payload={'full_name': customer.full_name},
		)

	def perform_update(self, serializer):
		customer = serializer.save()
		log_audit_event(
			tenant=self.request.tenant,
			actor=self.request.user,
			entity_type='customer',
			entity_id=customer.id,
			action='updated',
			payload={'full_name': customer.full_name},
		)

	def perform_destroy(self, instance):
		customer_id = instance.id
		customer_name = instance.full_name
		instance.delete()
		log_audit_event(
			tenant=self.request.tenant,
			actor=self.request.user,
			entity_type='customer',
			entity_id=customer_id,
			action='deleted',
			payload={'full_name': customer_name},
		)

# Create your views here.
