from django.db import connection
from django.utils.timezone import now
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthcheckView(APIView):
	permission_classes = [AllowAny]
	authentication_classes = []

	def get(self, request):
		with connection.cursor() as cursor:
			cursor.execute('SELECT 1')
			cursor.fetchone()

		return Response(
			{
				'status': 'ok',
				'timestamp': now().isoformat(),
				'services': {
					'database': 'ok',
				},
			}
		)