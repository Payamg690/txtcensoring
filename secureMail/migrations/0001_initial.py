# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-05 11:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_hash', models.CharField(max_length=255)),
                ('cyphertext', models.TextField()),
                ('pwd', models.CharField(max_length=255)),
            ],
        ),
    ]
