# Generated by Django 3.2 on 2022-06-01 02:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0012_zakaz_zakaz_goods_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zakaz',
            name='zakaz_goods_count',
        ),
    ]
