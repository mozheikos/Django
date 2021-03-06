# Generated by Django 3.2.10 on 2021-12-28 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=64, unique=True, verbose_name="Название категории")),
                ("description", models.TextField(blank=True, verbose_name="описание категории")),
            ],
        ),
    ]
