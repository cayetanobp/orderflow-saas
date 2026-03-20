from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import LogoutView, MeView
from customers.views import CustomerViewSet
from orders.views import OrderViewSet
from reporting.views import DashboardSummaryView
from tenants.views import CurrentTenantView, MembershipViewSet, TenantTokenObtainPairView
from config.views import HealthcheckView

router = DefaultRouter()
router.register('tenants/members', MembershipViewSet, basename='tenant-membership')
router.register('customers', CustomerViewSet, basename='customer')
router.register('orders', OrderViewSet, basename='order')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/health', HealthcheckView.as_view(), name='healthcheck'),
    path('api/v1/auth/login', TenantTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/logout', LogoutView.as_view(), name='auth-logout'),
    path('api/v1/auth/me', MeView.as_view(), name='auth-me'),
    path('api/v1/tenants/current', CurrentTenantView.as_view(), name='tenant-current'),
    path('api/v1/dashboard/summary', DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('api/v1/', include(router.urls)),
]
