from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save
from django.contrib.postgres.fields import ArrayField


class Vehicle(models.Model):
    is_active = models.BooleanField(
        null=False, blank=False, default=True, db_index=True)

    is_primary = models.BooleanField(default=True)
    vin = models.CharField(max_length=50, db_index=True)
    source_id = models.BigIntegerField(db_index=True)
    year = models.SmallIntegerField(db_index=True)
    make = models.CharField(max_length=50, db_index=True)
    model = models.CharField(max_length=150, db_index=True)
    trim = models.CharField(max_length=255, db_index=True)
    style = models.CharField(max_length=128)
    vehicle_type = models.CharField(max_length=24)
    body_type = models.CharField(max_length=32)
    body_subtype = models.CharField(max_length=32)
    doors = models.SmallIntegerField()
    msrp = models.IntegerField()
    plant = models.CharField(max_length=32)
    restraint_type = models.CharField(max_length=255)
    gvw_range = models.CharField(max_length=20)
    length = models.FloatField()
    height = models.FloatField()
    width = models.FloatField()
    wheelbase = models.FloatField()
    curb_weight = models.SmallIntegerField()
    gross_vehicle_weight_rating = models.IntegerField()
    tmp_wheel_dia = models.CharField(max_length=12)
    tmp_tank1_gal = models.CharField(max_length=6)
    max_payload = models.IntegerField()
    def_engine_id = models.IntegerField()
    drive_type = models.CharField(max_length=3)
    fuel_type = models.CharField(max_length=64)
    def_engine_block = models.CharField(max_length=1)
    def_engine_cylinders = models.SmallIntegerField()
    def_engine_size = models.FloatField()
    engine_size_uom = models.CharField(max_length=2)
    def_engine_aspiration = models.CharField(max_length=64)
    def_trans_id = models.IntegerField()
    def_trans_type = models.CharField(max_length=3)
    def_trans_speeds = models.SmallIntegerField()
    ext_color_name = models.TextField()
    ext_mfr_color_name = models.TextField()
    ext_mfr_color_code = models.TextField()
    ext_r_code = models.TextField()
    ext_g_code = models.TextField()
    ext_b_code = models.TextField()
    int_color_name = models.TextField()
    int_mfr_color_name = models.TextField()
    int_mfr_color_code = models.TextField()
    int_r_code = models.TextField()
    int_g_code = models.TextField()
    int_b_code = models.TextField()
    average_quadrant_premium = models.FloatField(default=0)

    def __str__(self):                                                                        
        return "%s : %s %s %s %s" % (
            self.id, self.year, self.make, self.model, self.style)

    def natural_key(self):
        return self.source_id, self.vin

    class Meta:
        unique_together = (('source_id', 'vin'),)


class Job(models.Model):
    job_scope = ArrayField(models.CharField())


class Garage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(_(""), max_length=254)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    specialty = ArrayField(models.CharField)
