# Generated by Django 4.2.6 on 2023-11-01 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_alter_videoproxy_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='vidoe_id',
            new_name='video_id',
        ),
    ]
