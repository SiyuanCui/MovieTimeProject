# Generated by Django 4.1.7 on 2023-08-15 22:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("reviewapp", "0005_review_stars_alter_review_text"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="review",
            name="rate",
        ),
    ]
