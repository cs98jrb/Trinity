# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailinf',
            name='subject',
            field=models.CharField(default=b"Website 'Contact Us'", max_length=128),
            preserve_default=True,
        ),
    ]
