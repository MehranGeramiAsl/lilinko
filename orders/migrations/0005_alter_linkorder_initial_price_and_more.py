# Generated by Django 4.2.7 on 2023-11-22 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_remove_linkorder_seller_linkorder_seller_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkorder',
            name='initial_price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='linkorder',
            name='updated_price',
            field=models.FloatField(default=0),
        ),
    ]