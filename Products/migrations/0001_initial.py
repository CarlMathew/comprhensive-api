# Generated by Django 5.1.5 on 2025-01-27 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('quantity_in_stock', models.IntegerField(default=0)),
                ('unit_price', models.DecimalField(decimal_places=2, default=2.0, max_digits=18)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'products',
                'managed': False,
            },
        ),
    ]
