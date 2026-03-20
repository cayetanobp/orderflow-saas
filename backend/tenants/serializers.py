from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import User
from tenants.models import Membership, Tenant


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ('id', 'name', 'slug', 'is_active')


class MembershipSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_first_name = serializers.CharField(source='user.first_name', read_only=True)
    user_last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Membership
        fields = ('id', 'user', 'user_email', 'user_first_name', 'user_last_name', 'role', 'created_at')
        read_only_fields = ('id', 'created_at', 'user_email', 'user_first_name', 'user_last_name')


class MembershipCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=Membership.Role.choices)

    def create(self, validated_data):
        tenant = self.context['tenant']
        email = validated_data['email']
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': validated_data.get('first_name', ''),
                'last_name': validated_data.get('last_name', ''),
            },
        )
        if created:
            user.set_unusable_password()
            user.save(update_fields=['password'])

        membership, _ = Membership.objects.update_or_create(
            tenant=tenant,
            user=user,
            defaults={'role': validated_data['role']},
        )
        return membership


class TenantTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token