# Generated by Django 3.2 on 2022-05-29 02:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0004_goods_goodstype'),
    ]

    operations = [
        migrations.AddField(
            model_name='zakaz',
            name='zakaz_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
