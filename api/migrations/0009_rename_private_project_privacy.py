# Generated by Django 5.1.3 on 2024-11-21 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_project_updated_at_alter_scene_text_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='private',
            new_name='privacy',
        ),
    ]
