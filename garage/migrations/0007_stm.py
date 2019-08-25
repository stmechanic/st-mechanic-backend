# Generated by Django 2.2 on 2019-08-25 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garage', '0006_stm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='make',
            field=models.CharField(db_index=True, default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='model',
            field=models.CharField(db_index=True, default='', max_length=150),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='vin',
            field=models.CharField(db_index=True, default='', max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='year',
            field=models.SmallIntegerField(db_index=True, default=2010),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='vehicle',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='source_id',
        ),
    ]
