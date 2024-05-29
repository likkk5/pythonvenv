# Generated by Django 5.0.4 on 2024-05-29 12:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Autosalon', '0007_order_price_alter_order_date_sold'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='promo_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_sold',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 29, 15, 55, 6, 95785)),
        ),
    ]
