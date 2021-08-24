# Generated by Django 3.2.6 on 2021-08-24 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_option'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeatClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('price', models.FloatField(default=0.0)),
            ],
            options={
                'verbose_name': 'seat_class',
            },
        ),
        migrations.DeleteModel(
            name='Seat',
        ),
    ]
