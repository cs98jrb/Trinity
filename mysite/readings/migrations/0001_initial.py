# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ref', models.CharField(default=b'x', max_length=8)),
                ('booked', models.DateField(auto_now_add=True, verbose_name=b'date booked')),
                ('Number of people', models.IntegerField()),
                ('confirmed', models.BooleanField(default=False)),
                ('payment_pending', models.BooleanField(default=False)),
                ('booked_by', models.ForeignKey(related_name='reading', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('value', models.DecimalField(max_digits=5, decimal_places=2)),
                ('online_book', models.BooleanField(default=False)),
                ('vat', models.ForeignKey(related_name='reading', to='orders.Vat')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='booking',
            name='price',
            field=models.ForeignKey(to='readings.Pricing'),
            preserve_default=True,
        ),
    ]
