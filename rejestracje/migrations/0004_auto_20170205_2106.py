# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-05 20:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rejestracje', '0003_auto_20170205_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='miejsceitermin',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
