# Generated by Django 3.2.6 on 2021-08-28 12:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0011_auto_20210827_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='create_datetime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]