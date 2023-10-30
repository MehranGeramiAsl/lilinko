# Generated by Django 4.2.6 on 2023-10-30 11:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0004_alter_user_options_alter_user_managers_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ResetPassword",
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
                ("email", models.CharField(max_length=255)),
                ("token", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="UserToken",
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
                ("user_id", models.IntegerField()),
                ("token", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("expired_at", models.DateTimeField()),
            ],
        ),
    ]