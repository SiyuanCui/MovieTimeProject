# Generated by Django 4.1.7 on 2023-08-16 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reviewapp", "0006_remove_review_rate"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="badge_level",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
