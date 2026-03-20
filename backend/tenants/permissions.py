from rest_framework.permissions import BasePermission

from tenants.models import Membership, Tenant


class HasTenantMembership(BasePermission):
    message = 'A valid tenant membership is required.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        tenant_slug = request.headers.get('X-Tenant-Slug')
        if tenant_slug:
            membership = Membership.objects.select_related('tenant').filter(
                tenant__slug=tenant_slug,
                tenant__is_active=True,
                user=request.user,
            ).first()
            if not membership:
                request.tenant = Tenant.objects.filter(slug=tenant_slug, is_active=True).first()
                request.membership = None
                return False
        else:
            membership = Membership.objects.select_related('tenant').filter(
                tenant__is_active=True,
                user=request.user,
            ).order_by('tenant__name').first()

        request.tenant = membership.tenant if membership else None
        request.membership = membership
        return bool(membership)


class IsTenantAdminOrOwner(BasePermission):
    message = 'Only tenant owners or admins can manage memberships.'

    def has_permission(self, request, view):
        membership = getattr(request, 'membership', None)
        if membership is None:
            return False

        return membership.role in {Membership.Role.OWNER, Membership.Role.ADMIN}