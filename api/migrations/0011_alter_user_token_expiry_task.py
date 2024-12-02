# Generated by Django 5.1.3 on 2024-12-02 05:02

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_calendar_color_event_color_alter_user_token_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='token_expiry',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 2, 5, 2, 28, 44222)),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the task', max_length=255)),
                ('status', models.CharField(choices=[('not_done', 'Not Done'), ('done', 'Done'), ('deleted', 'Deleted')], default='not_done', help_text='The status of the task', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='When the task was created')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='When the task was last updated')),
                ('user', models.ForeignKey(help_text='The user who created or owns this event', on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
