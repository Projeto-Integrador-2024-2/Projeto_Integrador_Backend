# Generated by Django 5.1.3 on 2024-12-10 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_rename_private_project_privacy'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='genres',
            field=models.ManyToManyField(related_name='projects', to='api.genre'),
        ),
    ]