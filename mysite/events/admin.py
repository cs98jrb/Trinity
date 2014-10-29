from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline


from events.models import Event, Venue, Priceing

class PriceingInline(admin.TabularInline):
    model = Priceing.event.through
    extra = 0

class EventAdmin(admin.ModelAdmin):
    inlines = [PriceingInline,]

admin.site.register(Event, EventAdmin)
admin.site.register(Venue)
admin.site.register(Priceing)