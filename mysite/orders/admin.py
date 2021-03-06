from django.contrib import admin
from orders.models import Order, OrderItem, Payment, Vat, PaymentType, Invoice


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [PaymentInline, OrderItemInline]


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'value', 'value_inc',)


class VatAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate_pc', 'used_rate')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Payment)
admin.site.register(Vat, VatAdmin)
admin.site.register(Invoice)
admin.site.register(PaymentType)