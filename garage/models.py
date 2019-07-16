"""Models for the Garaage module."""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class GarageUserManager(BaseUserManager):
    """Garage user Manager."""
    use_in_migrations = True

    def _create_user(self, **fields):
        """
        Create and save a user with the given email and national_idself.
        Use the national_id to set the initial password.
        The user will get a prompt tp update their password on log in.
        """
        email = fields.get('email')
        name = fields.get('name')
        password_one = fields.get('password1')
        password_two = fields.get('password2')

        if not email:
            raise ValueError("Email address is required")
        if not name:
            raise ValueError("Garage name is required")
        if password_one != password_two:
            raise ValueError("Both passwords need to match")

        email = self.normalize_email(email)
        user = self.model(**fields)
        user.save(using=self._db)
        return user

    def create_user(self, **fields):
        """."""
        fields.setdefault('is_staff', False)
        fields.setdefault('is_superuser', False)
        return self._create_user(**fields)

    def create_superuser(self, **fields):
        fields.setdefault('is_staff', True)
        fields.setdefault('is_superuser', True)

        if fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(**fields)


class Garage(AbstractBaseUser):
    """Represent a Garage."""
    name = models.CharField(max_length=255)
    username = None
    email = models.EmailField(unique=True, max_length=255)
    account_type = models.CharField(max_length=144, default='GARAGE')
    location = models.CharField(max_length=255, blank=True, null=True)
    verified = models.BooleanField(default=False)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    active = models.BooleanField(default=False)
    earnings = models.FloatField(default=0, blank=True)
    commission_percentage = models.FloatField(default=0, blank=True)
    commission = models.FloatField(default=0, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'registration_number', 'email']
    objects = GarageUserManager()

    @property
    def is_verified(self):
        return self.verified

    def verify(self):
        """
        verify a garage user account.
        An account is verified after the user has updated their password
        """
        self.verified = True
        self.save()
        return self.is_verified

    def to_dict(self):
        """Create a dict representation of a Garage."""
        return {
            'name': self.name,
            'specialty': self.specialties,
            'email': self.email,
            'registration_number': self.registration_number,
            'physical_address': self.physical_address
        }


class Vehicle(models.Model):
    """Represent a vehicle instance."""
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
    """Represent a vehicle job."""
    job_scope = models.TextField()
    garage = models.ForeignKey(
        Garage, on_delete=models.CASCADE, related_name='jobs')


class Specialty(models.Model):
    """Represent a Garage's specialty."""
    description = models.CharField(max_length=300)
    garage = models.ForeignKey(
        Garage, on_delete=models.CASCADE, related_name='specialties')
