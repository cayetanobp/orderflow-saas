from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from tenants.models import Membership
from tenants.permissions import HasTenantMembership, IsTenantAdminOrOwner
from tenants.serializers import (
	MembershipCreateSerializer,
	MembershipSerializer,
	TenantSerializer,
	TenantTokenObtainPairSerializer,
)


class TenantTokenObtainPairView(TokenObtainPairView):
	serializer_class = TenantTokenObtainPairSerializer


class CurrentTenantView(APIView):
	permission_classes = [IsAuthenticated, HasTenantMembership]

	def get(self, request):
		return Response(TenantSerializer(request.tenant).data)


class MembershipViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
	permission_classes = [IsAuthenticated, HasTenantMembership, IsTenantAdminOrOwner]

	def get_queryset(self):
		return Membership.objects.select_related('tenant', 'user').filter(tenant=self.request.tenant)

	def get_serializer_class(self):
		if self.action == 'create':
			return MembershipCreateSerializer
		return MembershipSerializer

	def get_serializer_context(self):
		context = super().get_serializer_context()
		context['tenant'] = self.request.tenant
		return context

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		membership = serializer.save()
		output = MembershipSerializer(membership)
		headers = self.get_success_headers(output.data)
		return Response(output.data, status=status.HTTP_201_CREATED, headers=headers)

# Create your views here.
