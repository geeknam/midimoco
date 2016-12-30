# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 03:27
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.manager
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity_id', models.UUIDField(db_index=True, default=uuid.uuid4)),
                ('checkpoint', models.IntegerField(db_index=True)),
                ('event_type', models.CharField(db_index=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('events_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='productevent',
            unique_together=set([('entity_id', 'checkpoint')]),
        ),
    ]