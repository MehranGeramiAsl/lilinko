# Generated by Django 4.2.6 on 2023-10-31 07:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("links", "0004_alter_link_dr_alter_link_traffic_linkprovider"),
    ]

    operations = [
        migrations.CreateModel(
            name="LinkCategories",
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
                ("title", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
