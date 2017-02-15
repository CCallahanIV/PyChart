# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-14 00:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pychart_datarender', '0003_data_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='render',
            name='data_sets',
            field=models.ManyToManyField(related_name='renders', to='pychart_datarender.Data'),
        ),
    ]