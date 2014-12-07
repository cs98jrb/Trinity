# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
        ('events', '0002_auto_20141204_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricing',
            name='vat',
            field=models.ForeignKey(default=1, to='orders.Vat'),
            preserve_default=False,
        ),
    ]
