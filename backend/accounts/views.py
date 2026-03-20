from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import CurrentUserSerializer
from tenants.models import Membership


class MeView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		memberships = Membership.objects.select_related('tenant').filter(user=request.user)
		serializer = CurrentUserSerializer(
			{
				'id': request.user.id,
				'email': request.user.email,
				'first_name': request.user.first_name,
				'last_name': request.user.last_name,
				'memberships': memberships,
			}
		)
		return Response(serializer.data)


class LogoutView(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request):
		return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.
