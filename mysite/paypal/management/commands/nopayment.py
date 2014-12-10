from django.core.management.base import BaseCommand, CommandError
from orders.models import Order


class Command(BaseCommand):
    help = 'Re open orders with failed payments'

    def handle(self, *args, **options):
        for order in Order.objects.failed_payment():
            order.waiting_payment = False
            order.save()
            self.stdout.write('Payment canceled "%s"' % order)