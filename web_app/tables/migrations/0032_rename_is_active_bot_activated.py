# Generated by Django 4.2.1 on 2023-05-17 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0031_delete_excludedwords_delete_keywords'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bot',
            old_name='is_active',
            new_name='activated',
        ),
    ]
