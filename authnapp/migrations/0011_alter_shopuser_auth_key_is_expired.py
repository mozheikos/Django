# Generated by Django 3.2.10 on 2022-02-13 13:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authnapp', '0010_alter_shopuser_auth_key_is_expired'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='auth_key_is_expired',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 2, 13, 13, 29, 35, 587894, tzinfo=utc)),
        ),
    ]
