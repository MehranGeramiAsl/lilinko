# Generated by Django 4.2.6 on 2023-11-01 07:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("links", "0008_linkrequest"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="link",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="link",
            name="updated_at",
        ),
        migrations.RemoveField(
            model_name="linkcategories",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="linkcategories",
            name="updated_at",
        ),
        migrations.RemoveField(
            model_name="linkprovider",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="linkprovider",
            name="updated_at",
        ),
        migrations.RemoveField(
            model_name="linkrequest",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="linkrequest",
            name="updated_at",
        ),
    ]
