# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20141211_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='payment_pending',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
