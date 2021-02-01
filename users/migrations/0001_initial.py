# Generated by Django 3.1.5 on 2021-02-01 11:08

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CashFoodMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('rugby_level', models.PositiveSmallIntegerField(default=0)),
                ('code', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(9999)])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Affilie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('code', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(9999)])),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.cashfoodmember')),
            ],
        ),
    ]
