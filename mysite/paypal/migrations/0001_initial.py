# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20141208_2050'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ref', models.CharField(max_length=50)),
                ('value', models.DecimalField(max_digits=6, decimal_places=2)),
                ('successful', models.DateTimeField(null=True, blank=True)),
                ('related_order', models.ForeignKey(related_name='paypal', to='orders.Order')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
