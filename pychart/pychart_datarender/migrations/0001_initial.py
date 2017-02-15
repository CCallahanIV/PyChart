# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 00:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pychart_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('data', models.FileField(blank=True, null=True, upload_to='data')),
                ('date_uploaded', models.DateField(auto_now=True)),
                ('date_modified', models.DateField(auto_now=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='data_sets', to='pychart_profile.PyChartProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Render',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('render_type', models.CharField(blank=True, choices=[('Scatter', 'Scatter'), ('Bar', 'Bar'), ('Histogram', 'Histogram')], max_length=255, null=True)),
                ('render', models.TextField(blank=True, null=True)),
                ('date_uploaded', models.DateField(auto_now=True)),
                ('date_modified', models.DateField(auto_now=True)),
                ('data_sets', models.ManyToManyField(related_name='renders', to='pychart_datarender.Data')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='renders', to='pychart_profile.PyChartProfile')),
            ],
        ),
    ]
