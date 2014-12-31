# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='lat',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=7, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='venue',
            name='lng',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=7, blank=True),
            preserve_default=True,
        ),
    ]
