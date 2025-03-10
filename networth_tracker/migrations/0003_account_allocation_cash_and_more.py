# Generated by Django 5.0.6 on 2024-06-17 10:50

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("networth_tracker", "0002_alter_customuser_date_joined_account_bankaccount"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="allocation_cash",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="account",
            name="allocation_cryptocurrency",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="account",
            name="allocation_etfs",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="account",
            name="allocation_intensity",
            field=models.PositiveSmallIntegerField(
                choices=[(0, "Light"), (1, "Normal"), (2, "Aggressive")], default=1
            ),
        ),
        migrations.AddField(
            model_name="account",
            name="allocation_managed_funds",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="account",
            name="allocation_other",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="account",
            name="allocation_stocks",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="account",
            name="date_of_birth",
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="account",
            name="emergency_fund",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="account",
            name="eoy_cash_goal",
            field=models.FloatField(default=50000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="account",
            name="long_term_tax_rate",
            field=models.FloatField(default=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="account",
            name="salary",
            field=models.FloatField(default=60000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="account",
            name="short_term_tax_rate",
            field=models.FloatField(default=0.15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="customuser",
            name="date_joined",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 6, 17, 10, 48, 12, 247780, tzinfo=datetime.timezone.utc
                ),
                verbose_name="date joined",
            ),
        ),
    ]
