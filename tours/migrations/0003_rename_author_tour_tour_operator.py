# Generated by Django 5.2 on 2025-05-01 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0002_alter_tour_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tour',
            old_name='author',
            new_name='tour_operator',
        ),
    ]
