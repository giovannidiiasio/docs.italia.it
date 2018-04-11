# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-04-11 10:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0008_add-project-relation'),
        ('docsitalia', '0003_auto_20180404_1053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publisher',
            name='remote_organization',
        ),
        migrations.AddField(
            model_name='publisher',
            name='remote_organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='oauth.RemoteOrganization', verbose_name='Remote organization'),
        ),
    ]