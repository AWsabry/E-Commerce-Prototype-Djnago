# Generated by Django 3.1.7 on 2022-02-10 01:15

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BromoCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('percentage', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'BromoCodes',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, upload_to='categories')),
                ('brand', models.CharField(blank=True, max_length=250)),
                ('description', models.TextField(blank=True)),
                ('featured', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, upload_to='products')),
                ('brand', models.CharField(blank=True, max_length=250)),
                ('description', models.TextField(blank=True)),
                ('price', models.PositiveIntegerField(default=0)),
                ('oldPrice', models.FloatField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('TopSelling', models.BooleanField(default=False)),
                ('NewProducts', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('stock', models.IntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories_and_products.category')),
            ],
            options={
                'verbose_name_plural': 'Products',
            },
        ),
    ]