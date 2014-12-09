# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20141209_1019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='value_exc',
        ),
    ]
