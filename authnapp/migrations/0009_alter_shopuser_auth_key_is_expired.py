# Generated by Django 3.2.10 on 2022-02-13 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authnapp', '0008_create_profiles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='auth_key_is_expired',
            field=models.DateTimeField(blank=True),
        ),
    ]
