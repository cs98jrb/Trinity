# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booked_by',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='event',
            field=models.ForeignKey(default=1, to='events.Event'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='price',
            field=models.ForeignKey(default=1, to='events.Pricing'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.ForeignKey(default=1, to='events.Venue'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pricing',
            name='vat',
            field=models.ForeignKey(default=1, to='orders.Vat'),
            preserve_default=False,
        ),
    ]
