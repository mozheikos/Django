# Generated by Django 3.2.10 on 2022-02-20 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_auto_20220215_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='discount',
            field=models.SmallIntegerField(default=0, verbose_name='Скидка'),
        ),
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.SmallIntegerField(default=0, verbose_name='Скидка'),
        ),
    ]