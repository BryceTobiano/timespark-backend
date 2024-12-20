# Generated by Django 5.1.3 on 2024-11-30 21:40

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_rename_is_all_day_event_allday_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(default=1, help_text='The user who created or owns this event', on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='token_expiry',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 30, 21, 40, 31, 818332)),
        ),
    ]
