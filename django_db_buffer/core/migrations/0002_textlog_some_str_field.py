# Generated by Django 4.2.4 on 2023-10-05 19:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="textlog",
            name="some_str_field",
            field=models.CharField(default="Strange reaction"),
        ),
    ]
