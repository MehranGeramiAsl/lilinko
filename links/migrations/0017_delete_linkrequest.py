# Generated by Django 4.2.6 on 2023-11-08 07:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("links", "0016_remove_linkcategories_link_link_categories"),
    ]

    operations = [
        migrations.DeleteModel(
            name="LinkRequest",
        ),
    ]