# Generated by Django 3.2.3 on 2022-05-28 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_and_orders', '0003_order_total_after_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='offerPercentage',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
