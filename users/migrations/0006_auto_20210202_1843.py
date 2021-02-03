# Generated by Django 3.1.5 on 2021-02-02 18:43

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210202_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashfoodmember',
            name='code',
            field=models.CharField(default='7PK0SOE7', max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='cashfoodmember',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, unique=True),
        ),
    ]
