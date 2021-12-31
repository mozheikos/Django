# Generated by Django 3.2.10 on 2021-12-31 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=120, verbose_name='город')),
                ('phone', models.CharField(max_length=15, verbose_name='телефон')),
                ('mail', models.EmailField(max_length=64, verbose_name='e-mail')),
                ('address', models.CharField(max_length=255, verbose_name='адрес')),
            ],
        ),
    ]
