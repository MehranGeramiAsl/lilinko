# Generated by Django 4.2.6 on 2023-11-06 08:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("links", "0013_alter_linkcategories_link"),
    ]

    operations = [
        migrations.AlterField(
            model_name="link",
            name="comment",
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]