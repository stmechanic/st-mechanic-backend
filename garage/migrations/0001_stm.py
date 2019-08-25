# Generated by Django 2.2 on 2019-05-26 11:33

from django.db import migrations, models
import django.db.models.deletion
import garage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Garage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('registration_number', models.CharField(max_length=20, unique=True)),
                ('physical_address', models.CharField(blank=True, max_length=255, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('opening_time', models.TimeField()),
                ('closing_time', models.TimeField()),
                ('active', models.BooleanField(default=False)),
                ('earnings', models.FloatField(blank=True, default=0)),
                ('commission_percentage', models.FloatField(blank=True, default=0)),
                ('commission', models.FloatField(blank=True, default=0)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', garage.models.GarageUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('is_primary', models.BooleanField(default=True)),
                ('vin', models.CharField(db_index=True, max_length=50)),
                ('source_id', models.BigIntegerField(db_index=True)),
                ('year', models.SmallIntegerField(db_index=True)),
                ('make', models.CharField(db_index=True, max_length=50)),
                ('model', models.CharField(db_index=True, max_length=150)),
                ('trim', models.CharField(db_index=True, max_length=255)),
                ('style', models.CharField(max_length=128)),
                ('vehicle_type', models.CharField(max_length=24)),
                ('body_type', models.CharField(max_length=32)),
                ('body_subtype', models.CharField(max_length=32)),
                ('doors', models.SmallIntegerField()),
                ('msrp', models.IntegerField()),
                ('plant', models.CharField(max_length=32)),
                ('restraint_type', models.CharField(max_length=255)),
                ('gvw_range', models.CharField(max_length=20)),
                ('length', models.FloatField()),
                ('height', models.FloatField()),
                ('width', models.FloatField()),
                ('wheelbase', models.FloatField()),
                ('curb_weight', models.SmallIntegerField()),
                ('gross_vehicle_weight_rating', models.IntegerField()),
                ('tmp_wheel_dia', models.CharField(max_length=12)),
                ('tmp_tank1_gal', models.CharField(max_length=6)),
                ('max_payload', models.IntegerField()),
                ('def_engine_id', models.IntegerField()),
                ('drive_type', models.CharField(max_length=3)),
                ('fuel_type', models.CharField(max_length=64)),
                ('def_engine_block', models.CharField(max_length=1)),
                ('def_engine_cylinders', models.SmallIntegerField()),
                ('def_engine_size', models.FloatField()),
                ('engine_size_uom', models.CharField(max_length=2)),
                ('def_engine_aspiration', models.CharField(max_length=64)),
                ('def_trans_id', models.IntegerField()),
                ('def_trans_type', models.CharField(max_length=3)),
                ('def_trans_speeds', models.SmallIntegerField()),
                ('ext_color_name', models.TextField()),
                ('ext_mfr_color_name', models.TextField()),
                ('ext_mfr_color_code', models.TextField()),
                ('ext_r_code', models.TextField()),
                ('ext_g_code', models.TextField()),
                ('ext_b_code', models.TextField()),
                ('int_color_name', models.TextField()),
                ('int_mfr_color_name', models.TextField()),
                ('int_mfr_color_code', models.TextField()),
                ('int_r_code', models.TextField()),
                ('int_g_code', models.TextField()),
                ('int_b_code', models.TextField()),
                ('average_quadrant_premium', models.FloatField(default=0)),
            ],
            options={
                'unique_together': {('source_id', 'vin')},
            },
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=300)),
                ('garage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specialties', to='garage.Garage')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_scope', models.TextField()),
                ('garage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='garage.Garage')),
            ],
        ),
    ]