# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-08-04 18:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_remove_order_p_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_delete',
            field=models.BooleanField(default=0, verbose_name='是否删除'),
        ),
    ]
