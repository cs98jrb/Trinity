# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20141029_1326'),
    ]

    operations = [
        migrations.RenameField(
            model_name='venue',
            old_name='town1',
            new_name='town',
        ),
    ]
