# Generated by Django 2.2 on 2019-05-27 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garage', '0002_stm'),
    ]

    operations = [
        migrations.RenameField(
            model_name='garage',
            old_name='physical_address',
            new_name='location',
        ),
    ]
