# Generated by Django 5.1.3 on 2024-11-30 09:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_user_token_expiry_category_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='is_all_day',
            new_name='allDay',
        ),
        migrations.AlterField(
            model_name='user',
            name='token_expiry',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 30, 9, 3, 55, 714573)),
        ),
    ]
