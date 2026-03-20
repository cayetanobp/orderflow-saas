from decimal import Decimal

from django.core.management.base import BaseCommand

from accounts.models import User
from customers.models import Customer
from orders.models import Order, OrderItem, OrderStatusHistory
from tenants.models import Membership, Tenant


class Command(BaseCommand):
    help = 'Seed a local demo tenant with users, customers, and orders.'

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            email='owner@example.com',
            defaults={
                'first_name': 'Demo',
                'last_name': 'Owner',
                'is_staff': True,
            },
        )
        if created:
            user.set_password('change-me')
            user.save(update_fields=['password'])

        tenant, _ = Tenant.objects.get_or_create(name='Northwind Print', slug='northwind-print')
        Membership.objects.get_or_create(tenant=tenant, user=user, role=Membership.Role.OWNER)

        customer, _ = Customer.objects.get_or_create(
            tenant=tenant,
            full_name='Alicia Stone',
            defaults={
                'email': 'alicia@example.com',
                'company_name': 'Stone Interiors',
                'phone': '+34 600 000 000',
            },
        )

        order, created = Order.objects.get_or_create(
            tenant=tenant,
            code='NW-1001',
            defaults={
                'customer': customer,
                'title': 'Retail facade lettering',
                'description': 'Production and installation for the spring campaign.',
                'priority': Order.Priority.HIGH,
                'status': Order.Status.CONFIRMED,
                'created_by': user,
                'total_amount': Decimal('240.00'),
            },
        )
        if created:
            OrderItem.objects.create(order=order, name='Design', quantity=1, unit_price=Decimal('90.00'), notes='')
            OrderItem.objects.create(order=order, name='Production', quantity=1, unit_price=Decimal('150.00'), notes='')
            OrderStatusHistory.objects.create(
                order=order,
                from_status='',
                to_status=Order.Status.CONFIRMED,
                changed_by=user,
                note='Demo order created',
            )

        self.stdout.write(self.style.SUCCESS('Demo data ready.'))
        self.stdout.write('Email: owner@example.com')
        self.stdout.write('Password: change-me')
        self.stdout.write('Tenant header: northwind-print')