# Generated by Django 3.2 on 2022-05-30 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0005_zakaz_zakaz_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zakaz',
            name='zakaz_time',
            field=models.DateTimeField(verbose_name='Время добавления'),
        ),
    ]