# Generated by Django 4.2.6 on 2023-10-31 07:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("links", "0005_linkcategories"),
    ]

    operations = [
        migrations.AddField(
            model_name="linkcategories",
            name="link",
            field=models.ManyToManyField(related_name="link", to="links.link"),
        ),
    ]
