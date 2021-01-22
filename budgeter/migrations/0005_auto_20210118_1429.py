# Generated by Django 3.1.4 on 2021-01-18 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgeter', '0004_auto_20210117_2018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactionlist',
            name='starting_budget',
        ),
        migrations.AddField(
            model_name='transactionlist',
            name='starting_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date_posted',
            field=models.DateField(),
        ),
    ]