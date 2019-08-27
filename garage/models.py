"""Models for the Garaage module."""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from garage.enums import JobStatus, QuoteStatus


class GarageUserManager(BaseUserManager):
    """Garage user Manager."""
    use_in_migrations = True

    def _create_user(self, **fields):
        """
        Create and save a user with the given email.
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
        user.set_password(password_one)
        user.save(using=self._db)
        return user

    def create_user(self, **fields):
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
    registration_number = models.CharField(max_length=144, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    verified = models.BooleanField(default=False)
    opening_time = models.TimeField(null=True)
    closing_time = models.TimeField(null=True)
    active = models.BooleanField(default=False)
    earnings = models.FloatField(default=0, blank=True, null=True)
    commission_percentage = models.FloatField(default=0, blank=True, null=True)
    commission = models.FloatField(default=0, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'registration_number']
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
        }


class Vehicle(models.Model):
    """Represent a vehicle instance."""
    is_active = models.BooleanField(
        null=False, blank=False, default=True, db_index=True)
    is_primary = models.BooleanField(default=True, null=True)
    year = models.SmallIntegerField(db_index=True)
    make = models.CharField(max_length=50, db_index=True)
    model = models.CharField(max_length=150, db_index=True)
    vin = models.CharField(max_length=50, db_index=True, unique=True)
    trim = models.CharField(max_length=255, db_index=True, null=True)
    style = models.CharField(max_length=128, null=True)
    vehicle_type = models.CharField(max_length=24, null=True)
    body_type = models.CharField(max_length=32, null=True)
    body_subtype = models.CharField(max_length=32, null=True)
    doors = models.SmallIntegerField(null=True)
    msrp = models.IntegerField(null=True)
    plant = models.CharField(max_length=32, null=True)
    restraint_type = models.CharField(max_length=255, null=True)
    gvw_range = models.CharField(max_length=20, null=True)
    length = models.FloatField(null=True)
    height = models.FloatField(null=True)
    width = models.FloatField(null=True)
    wheelbase = models.FloatField(null=True)
    curb_weight = models.SmallIntegerField(null=True)
    gross_vehicle_weight_rating = models.IntegerField(null=True)
    tmp_wheel_dia = models.CharField(max_length=12, null=True)
    tmp_tank1_gal = models.CharField(max_length=6, null=True)
    max_payload = models.IntegerField(null=True)
    def_engine_id = models.IntegerField(null=True)
    drive_type = models.CharField(max_length=3, null=True)
    fuel_type = models.CharField(max_length=64, null=True)
    def_engine_block = models.CharField(max_length=1, null=True)
    def_engine_cylinders = models.SmallIntegerField(null=True)
    def_engine_size = models.FloatField(null=True)
    engine_size_uom = models.CharField(max_length=2, null=True)
    def_engine_aspiration = models.CharField(max_length=64, null=True)
    def_trans_id = models.IntegerField(null=True)
    def_trans_type = models.CharField(max_length=3, null=True)
    def_trans_speeds = models.SmallIntegerField(null=True)
    ext_color_name = models.TextField(null=True)
    ext_mfr_color_name = models.TextField(null=True)
    ext_mfr_color_code = models.TextField(null=True)
    ext_r_code = models.TextField(null=True)
    ext_g_code = models.TextField(null=True)
    ext_b_code = models.TextField(null=True)
    int_color_name = models.TextField(null=True)
    int_mfr_color_name = models.TextField(null=True)
    int_mfr_color_code = models.TextField(null=True)
    int_r_code = models.TextField(null=True)
    int_g_code = models.TextField(null=True)
    int_b_code = models.TextField(null=True)
    average_quadrant_premium = models.FloatField(default=0, null=True)

    def __str__(self):
        return f'{self.id}, {self.year}, {self.make}, {self.model}'


class Mechanic(models.Model):
    name = models.CharField(max_length=300)
    email = models.CharField(max_length=300)
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE, related_name='mechanics')


class Job(models.Model):
    """Represent a vehicle job."""
    job_scope = models.TextField()
    garage = models.ForeignKey(
        Garage, on_delete=models.CASCADE, related_name='jobs')
    customer_name = models.CharField(max_length=144)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='jobs', null=True)
    status = models.CharField(
        max_length=50,
        choices=[(tag, tag.value) for tag in JobStatus],
        default=JobStatus.INCOMING
    )
    mechanic = models.ForeignKey(Mechanic, on_delete=models.SET_NULL, related_name='jobs', null=True)


class Quote(models.Model):
    amount = models.FloatField(default=0, blank=True)
    status = models.CharField(
        max_length=100,
        choices=[(tag, tag.value) for tag in QuoteStatus],
        default=QuoteStatus.OPEN
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='submitted_quotes')
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE, related_name='quotes')


class Rating(models.Model):
    comment = models.CharField(max_length=255)
    customer = models.CharField(max_length=144)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='ratings')


class Specialty(models.Model):
    """Represent a Garage's specialty."""
    description = models.CharField(max_length=300)
    garage = models.ForeignKey(
        Garage, on_delete=models.CASCADE, related_name='specialties')


