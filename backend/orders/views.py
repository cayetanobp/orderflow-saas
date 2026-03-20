from rest_framework import decorators, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from audit.services import log_audit_event
from orders.models import Order, OrderStatusHistory
from orders.serializers import OrderSerializer, OrderStatusHistorySerializer, OrderTransitionSerializer
from tenants.permissions import HasTenantMembership


class OrderViewSet(viewsets.ModelViewSet):
	serializer_class = OrderSerializer
	permission_classes = [IsAuthenticated, HasTenantMembership]
	filterset_fields = ('status', 'priority', 'customer')
	search_fields = ('code', 'title', 'customer__full_name')
	ordering_fields = ('created_at', 'updated_at', 'due_date', 'code')
	ordering = ('-created_at',)

	def get_queryset(self):
		return Order.objects.select_related('customer', 'created_by').prefetch_related('items', 'history').filter(
			tenant=self.request.tenant
		)

	def perform_create(self, serializer):
		order = serializer.save(tenant=self.request.tenant, created_by=self.request.user)
		log_audit_event(
			tenant=self.request.tenant,
			actor=self.request.user,
			entity_type='order',
			entity_id=order.id,
			action='created',
			payload={'code': order.code, 'status': order.status},
		)

	def perform_update(self, serializer):
		order = serializer.save()
		log_audit_event(
			tenant=self.request.tenant,
			actor=self.request.user,
			entity_type='order',
			entity_id=order.id,
			action='updated',
			payload={'code': order.code, 'status': order.status},
		)

	@decorators.action(detail=True, methods=['post'])
	def transition(self, request, pk=None):
		order = self.get_object()
		serializer = OrderTransitionSerializer(data=request.data, context={'order': order})
		serializer.is_valid(raise_exception=True)

		from_status = order.status
		order.status = serializer.validated_data['to_status']
		order.save(update_fields=['status', 'updated_at'])

		history_entry = OrderStatusHistory.objects.create(
			order=order,
			from_status=from_status,
			to_status=order.status,
			changed_by=request.user,
			note=serializer.validated_data.get('note', ''),
		)
		log_audit_event(
			tenant=request.tenant,
			actor=request.user,
			entity_type='order',
			entity_id=order.id,
			action='transitioned',
			payload={'code': order.code, 'from_status': from_status, 'to_status': order.status},
		)
		return Response(OrderStatusHistorySerializer(history_entry).data, status=status.HTTP_200_OK)

	@decorators.action(detail=True, methods=['get'])
	def history(self, request, pk=None):
		order = self.get_object()
		serializer = OrderStatusHistorySerializer(order.history.all(), many=True)
		return Response(serializer.data)

# Create your views here.
