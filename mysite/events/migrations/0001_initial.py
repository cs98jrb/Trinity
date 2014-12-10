# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ref', models.CharField(default=b'x', max_length=8)),
                ('booked', models.DateField(auto_now_add=True, verbose_name=b'date booked')),
                ('quantity', models.IntegerField()),
                ('confirmed', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('capacity', models.IntegerField(default=0)),
                ('event_time', models.DateTimeField()),
                ('book_from', models.DateTimeField(null=True, blank=True)),
                ('last_booking', models.DateTimeField()),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name=b'date published')),
            ],
            options={
                'ordering': ['event_time'],
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
                ('event', models.ManyToManyField(to='events.Event', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('town', models.CharField(max_length=50)),
                ('postcode', models.CharField(max_length=8, blank=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
