# Generated by Django 3.2.6 on 2021-08-27 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_ticket_customer_ti_ticket__6572c1_idx'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='name_passenger',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='ticket',
            name='last_name',
            field=models.CharField(default=1, max_length=256),
            preserve_default=False,
        ),
    ]
