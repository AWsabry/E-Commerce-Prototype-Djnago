# Generated by Django 3.2.3 on 2022-05-20 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_and_orders', '0002_auto_20220428_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_after_offer',
            field=models.PositiveIntegerField(default=0),
        ),
    ]