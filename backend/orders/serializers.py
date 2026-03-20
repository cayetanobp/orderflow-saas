from decimal import Decimal

from rest_framework import serializers

from orders.models import Order, OrderItem, OrderStatusHistory


ALLOWED_STATUS_TRANSITIONS = {
    Order.Status.DRAFT: {Order.Status.CONFIRMED, Order.Status.CANCELED},
    Order.Status.CONFIRMED: {Order.Status.IN_PROGRESS, Order.Status.CANCELED},
    Order.Status.IN_PROGRESS: {Order.Status.AWAITING_REVIEW, Order.Status.CANCELED},
    Order.Status.AWAITING_REVIEW: {Order.Status.IN_PROGRESS, Order.Status.COMPLETED, Order.Status.CANCELED},
    Order.Status.COMPLETED: {Order.Status.DELIVERED},
    Order.Status.DELIVERED: set(),
    Order.Status.CANCELED: set(),
}


def is_valid_status_transition(from_status, to_status):
    return to_status in ALLOWED_STATUS_TRANSITIONS.get(from_status, set())


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'name', 'quantity', 'unit_price', 'notes')
        read_only_fields = ('id',)


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    changed_by_email = serializers.EmailField(source='changed_by.email', read_only=True)

    class Meta:
        model = OrderStatusHistory
        fields = ('id', 'from_status', 'to_status', 'changed_by', 'changed_by_email', 'changed_at', 'note')
        read_only_fields = ('id', 'changed_by', 'changed_by_email', 'changed_at')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=False)
    history = OrderStatusHistorySerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'customer',
            'customer_name',
            'code',
            'title',
            'description',
            'status',
            'priority',
            'due_date',
            'total_amount',
            'created_by',
            'created_at',
            'updated_at',
            'items',
            'history',
        )
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at', 'history', 'customer_name')

    def validate_customer(self, value):
        tenant = self.context['request'].tenant
        if value.tenant_id != tenant.id:
            raise serializers.ValidationError('Customer does not belong to the active tenant.')
        return value

    def validate_items(self, value):
        if not value:
            return value

        for item in value:
            if item['quantity'] < 1:
                raise serializers.ValidationError('Item quantity must be at least 1.')
        return value

    def validate(self, attrs):
        attrs = super().validate(attrs)
        instance = getattr(self, 'instance', None)
        if not instance:
            return attrs

        next_status = attrs.get('status', instance.status)
        if next_status != instance.status and not is_valid_status_transition(instance.status, next_status):
            raise serializers.ValidationError(
                {
                    'status': (
                        f'Invalid status transition from "{instance.status}" to "{next_status}". '
                        'Use a valid workflow transition.'
                    )
                }
            )

        return attrs

    def _sync_items(self, order, items_data):
        order.items.all().delete()
        total_amount = Decimal('0.00')
        for item_data in items_data:
            order_item = OrderItem.objects.create(order=order, **item_data)
            total_amount += order_item.unit_price * order_item.quantity
        order.total_amount = total_amount
        order.save(update_fields=['total_amount', 'updated_at'])

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)
        if items_data:
            self._sync_items(order, items_data)
        OrderStatusHistory.objects.create(
            order=order,
            from_status='',
            to_status=order.status,
            changed_by=order.created_by,
            note='Initial status',
        )
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        previous_status = instance.status
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        if items_data is not None:
            self._sync_items(instance, items_data)

        if previous_status != instance.status:
            OrderStatusHistory.objects.create(
                order=instance,
                from_status=previous_status,
                to_status=instance.status,
                changed_by=self.context['request'].user,
                note='Status changed during update',
            )

        return instance


class OrderTransitionSerializer(serializers.Serializer):
    to_status = serializers.ChoiceField(choices=Order.Status.choices)
    note = serializers.CharField(required=False, allow_blank=True)

    def validate_to_status(self, value):
        order = self.context['order']
        if order.status == value:
            raise serializers.ValidationError('Order is already in that status.')
        if not is_valid_status_transition(order.status, value):
            raise serializers.ValidationError(
                f'Invalid status transition from "{order.status}" to "{value}".'
            )
        return value