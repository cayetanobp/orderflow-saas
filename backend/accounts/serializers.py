from rest_framework import serializers

from tenants.models import Membership


class MembershipSummarySerializer(serializers.ModelSerializer):
    tenant_id = serializers.IntegerField(source='tenant.id', read_only=True)
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    tenant_slug = serializers.CharField(source='tenant.slug', read_only=True)

    class Meta:
        model = Membership
        fields = ('id', 'role', 'tenant_id', 'tenant_name', 'tenant_slug')


class CurrentUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    memberships = MembershipSummarySerializer(many=True, read_only=True)