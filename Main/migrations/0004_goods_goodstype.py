# Generated by Django 3.2 on 2022-05-29 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0003_cart_zakaz'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='GoodsType',
            field=models.CharField(blank=True, choices=[('US', 'United States'), ('FR', 'France'), ('CN', 'China'), ('RU', 'Russia'), ('IT', 'Italy')], max_length=300, null=True),
        ),
    ]
