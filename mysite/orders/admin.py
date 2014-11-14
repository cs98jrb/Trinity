from django.contrib import admin
from orders.models import Order, OrderItem, Payment


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [PaymentInline, OrderItemInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Payment)