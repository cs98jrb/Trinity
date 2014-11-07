from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline


from mysite.models import EmailInf


admin.site.register(EmailInf)