# Generated by Django 3.2.3 on 2021-10-03 20:47

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Register_Login', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='being_delivered',
            new_name='delivered',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='received',
            new_name='paid',
        ),
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='item',
        ),
        migrations.AddField(
            model_name='order',
            name='product_name',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='orders',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='Register_Login.order'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.CASCADE, related_name='item', to='Register_Login.product'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bromocode',
            name='percentage',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='totalOrderItemPrice',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.UUIDField(default=uuid.UUID('88ff1ff8-0c43-4a5a-9d6f-ea6ae36d0f74'), editable=False, primary_key=True, serialize=False),
        ),
    ]
