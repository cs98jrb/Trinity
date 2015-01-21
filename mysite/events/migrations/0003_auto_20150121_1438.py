# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20141228_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=ckeditor.fields.RichTextField(),
            preserve_default=True,
        ),
    ]
