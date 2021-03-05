# Generated by Django 3.1.5 on 2021-03-05 10:18

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20210304_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sbfmember',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Numero de Telephone'),
        ),
    ]
