# Generated by Django 5.0.4 on 2024-05-29 11:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Autosalon', '0005_contact_product_photo_alter_order_date_sold'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_sold',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 29, 14, 48, 46, 495369)),
        ),
    ]
