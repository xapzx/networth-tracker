# Generated by Django 5.0.6 on 2024-06-10 04:36

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("networth_tracker", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="date_joined",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 6, 10, 4, 36, 56, 473035, tzinfo=datetime.timezone.utc
                ),
                verbose_name="date joined",
            ),
        ),
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("first_name", models.CharField(max_length=64)),
                ("last_name", models.CharField(max_length=64)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BankAccount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("bank", models.CharField(max_length=100)),
                ("account_name", models.CharField(max_length=100)),
                ("balance", models.FloatField()),
                ("interest_rate", models.FloatField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
    ]
