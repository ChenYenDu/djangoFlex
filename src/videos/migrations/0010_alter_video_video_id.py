# Generated by Django 4.2.6 on 2023-11-07 16:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("videos", "0009_video_timestamp_video_updated"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="video_id",
            field=models.CharField(max_length=220, unique=True),
        ),
    ]