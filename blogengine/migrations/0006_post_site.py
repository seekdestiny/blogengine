# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-17 05:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('blogengine', '0005_remove_post_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='site',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sites.Site'),
            preserve_default=False,
        ),
    ]
