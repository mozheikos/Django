# Generated by Django 3.2.10 on 2022-01-19 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authnapp", "0003_alter_shopuser_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shopuser",
            name="avatar",
            field=models.ImageField(blank=True, upload_to="users_avatars"),
        ),
    ]
