from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from audit.models import AuditEvent
from orders.models import Order, OrderStatusHistory
from tenants.permissions import HasTenantMembership


class DashboardSummaryView(APIView):
	permission_classes = [IsAuthenticated, HasTenantMembership]

	def get(self, request):
		tenant_orders = Order.objects.filter(tenant=request.tenant)
		orders_by_status = list(tenant_orders.values('status').annotate(count=Count('id')).order_by('status'))
		recent_activity = list(
			OrderStatusHistory.objects.filter(order__tenant=request.tenant)
			.select_related('changed_by', 'order')
			.order_by('-changed_at')[:10]
			.values('id', 'order_id', 'order__code', 'from_status', 'to_status', 'changed_at', 'changed_by__email')
		)
		audit_count = AuditEvent.objects.filter(tenant=request.tenant).count()

		return Response(
			{
				'totals': {
					'customers': request.tenant.customers.count(),
					'orders': tenant_orders.count(),
					'audit_events': audit_count,
				},
				'orders_by_status': orders_by_status,
				'recent_activity': recent_activity,
			}
		)

# Create your views here.
