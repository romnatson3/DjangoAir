# Generated by Django 3.2.6 on 2021-08-26 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_flight_gate'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='gateway_passed',
            field=models.BooleanField(default=False),
        ),
    ]
