# Generated by Django 5.0.2 on 2024-03-31 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='lecture',
        ),
        migrations.DeleteModel(
            name='Lecture',
        ),
    ]
