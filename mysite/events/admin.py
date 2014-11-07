from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline


from events.models import Event, Venue, Pricing

class PricingInline(admin.TabularInline):
    model = Pricing.event.through
    extra = 0

class EventAdmin(admin.ModelAdmin):
    inlines = [PricingInline,]

admin.site.register(Event, EventAdmin)
admin.site.register(Venue)
admin.site.register(Pricing)