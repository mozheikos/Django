# Generated by Django 3.2.10 on 2022-02-02 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ordersapp", "0001_orders"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="is_actie",
            new_name="is_active",
        ),
    ]
