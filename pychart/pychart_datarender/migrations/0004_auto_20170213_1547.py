# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-13 23:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pychart_profile', '0001_initial'),
        ('pychart_datarender', '0003_auto_20170213_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='data_sets', to='pychart_profile.PyChartProfile'),
        ),
        migrations.AddField(
            model_name='render',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='renderss', to='pychart_profile.PyChartProfile'),
        ),
    ]
