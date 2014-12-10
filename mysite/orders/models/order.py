from django.db import models
from django.conf import settings
from django.db.models import Min, Sum, Count
from django.utils import timezone
from datetime import timedelta


class OrderManager(models.Manager):
    def failed_payment(self):
        return super(OrderManager, self).get_queryset().filter(
            waiting_payment=True,
            open=True,
            last_change__lt=(timezone.now() - timedelta(minutes=settings.PAYPAL_HOLD_BOOKING))
        )

    def open_order(self, user):
        return super(OrderManager, self).get_queryset().filter(open=True, ordered_by=user)


class Order(models.Model):
    date = models.DateField(auto_now_add=True)
    open = models.BooleanField(default=True)
    ordered_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    objects = OrderManager()
    last_change = models.DateTimeField(auto_now=True)
    waiting_payment = models.BooleanField(default=False)

    @property
    def total_ex(self):
        ex_vat_dict = self.orderitem_set.all().aggregate(exvat=Sum('value'))
        return ex_vat_dict['exvat']

    @property
    def total_inc(self):
        if not settings.VAT_REGISTERED:
            ex_vat_dict = self.orderitem_set.all().aggregate(exvat=Sum('value'))
            return ex_vat_dict['exvat']
        vat_list = self.orderitem_set.order_by('vat').values('vat__rate').annotate(exvat=Sum('value'))
        total_inc = 0
        for vat in vat_list:
            total_inc += round(vat['exvat'] * (1+vat['vat__rate']), 2)
        return total_inc

    @property
    def vat_inf(self):
        if not settings.VAT_REGISTERED:
            return

        vat_list = self.orderitem_set.order_by('vat').values('vat__rate', 'vat__name').annotate(
            exvat=Sum('value')
        )
        for vat in vat_list:
            vat['vat_val'] = round(vat['exvat'] * (vat['vat__rate']), 2)
            vat['rate_pc'] = vat['vat__rate'] * 100
        return vat_list

    @property
    def vat_num(self):
        return settings.VAT_REGISTERED

    def save(self, *args, **kwargs):
        if not self.open or self.waiting_payment:
            status = True
        else:
            status = False

        for order_item in self.orderitem_set.all():
            print(order_item.content_object)
            order_item.content_object.confirmed = status
            order_item.content_object.save()

        super(Order, self).save(*args, **kwargs)

    def __unicode__(self):  # __unicode__ on Python 2
        return str(self.pk) + " " + self.date.strftime('%d/%m/%Y')
