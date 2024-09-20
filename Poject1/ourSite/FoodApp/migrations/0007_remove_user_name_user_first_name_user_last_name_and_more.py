# Generated by Django 5.1.1 on 2024-09-19 21:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("FoodApp", "0006_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="name",
        ),
        migrations.AddField(
            model_name="user",
            name="first_name",
            field=models.CharField(default="Unknown first_name", max_length=70),
        ),
        migrations.AddField(
            model_name="user",
            name="last_name",
            field=models.CharField(default="Unknown last_name", max_length=70),
        ),
        migrations.AddField(
            model_name="user",
            name="username",
            field=models.CharField(
                default="Unknown username", max_length=70, unique=True
            ),
        ),
    ]
