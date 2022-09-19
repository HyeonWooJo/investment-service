# Generated by Django 4.1.1 on 2022-09-19 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Holding",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=40)),
                ("isin", models.CharField(max_length=70)),
                (
                    "current_price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=8),
                ),
                ("asset_group", models.CharField(max_length=40)),
            ],
            options={
                "db_table": "holdings",
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20, verbose_name="이름")),
            ],
            options={
                "db_table": "users",
            },
        ),
        migrations.CreateModel(
            name="UserHolding",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField()),
                (
                    "holding",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="apis.holding"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="apis.user"
                    ),
                ),
            ],
            options={
                "db_table": "user_holdings",
            },
        ),
        migrations.CreateModel(
            name="Investment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("company", models.CharField(max_length=40)),
                (
                    "principal",
                    models.DecimalField(decimal_places=2, default=0, max_digits=15),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="apis.user"
                    ),
                ),
            ],
            options={
                "db_table": "investment",
            },
        ),
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("account_name", models.CharField(max_length=40)),
                ("account_number", models.PositiveIntegerField()),
                (
                    "total_assessts",
                    models.DecimalField(decimal_places=2, default=0, max_digits=15),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="apis.user"
                    ),
                ),
            ],
            options={
                "db_table": "accounts",
            },
        ),
    ]