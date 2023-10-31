# Generated by Django 4.2.6 on 2023-10-31 07:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("links", "0006_linkcategories_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="linkcategories",
            name="link_provider",
            field=models.ManyToManyField(
                related_name="link_provider", to="links.linkprovider"
            ),
        ),
    ]