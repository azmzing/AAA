# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-07-03 11:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AXF', '0003_homemustbuy'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeShop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=32)),
                ('trackid', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'axf_shop',
            },
        ),
    ]
