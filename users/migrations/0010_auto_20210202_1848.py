# Generated by Django 3.1.5 on 2021-02-02 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20210202_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashfoodmember',
            name='code',
            field=models.CharField(default='XQ6BJP03', max_length=8, unique=True),
        ),
    ]
