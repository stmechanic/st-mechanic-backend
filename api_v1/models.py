from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, **fields):
        """
        Create and save a user with the given email and national_idself.
        Use the national_id to set the initial password.
        The user will get a prompt tp update their password on log in.
        """
        email = fields.get('email')
        national_id = fields.get('national_id')
        date_of_birth = fields.get('date_of_birth')
        if not email:
            raise ValueError("Email address is required")
        if not national_id:
            raise ValueError("National Id Number is required")
        if not date_of_birth:
            raise ValueError("Date of birth is required")

        email = self.normalize_email(email)
        user = self.model(**fields)
        # set the national_id as the temporary password
        user.set_one_time_password(national_id)
        user.save(using=self._db)
        return user

    def create_user(self, **fields):
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


class Customer(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    national_id = models.CharField(max_length=20, unique=True)
    picture = models.ImageField(upload_to='images/', blank=True, null=True)
    date_of_birth = models.DateField(
        auto_now=False, auto_now_add=False, blank=False, unique=False)
    physical_address = models.CharField(max_length=255, blank=True, null=True)
    verified = models.BooleanField(default=False)
    proof_of_address = models.FileField(
        upload_to='files/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name', 'last_name', 'national_id', 'date_of_birth'
    ]
    objects = UserManager()

    @property
    def is_verified(self):
        return self.verified

    def verify(self, old_password, new_password):
        """
        verify a user account.
        An account is verified after the user has updated their password
        """
        if self.check_password(old_password):
            self.set_password(new_password)
            self.verified = self.check_password(new_password)
            self.save()
            return self.is_verified
        else:
            raise ValueError('Incorrect password')

    def set_one_time_password(self, temporary_password):
        """
        Set a temporary password.
        """
        self.set_password(temporary_password)
        self.save()

    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'national_id': self.national_id,
            'date_of_birth': str(self.date_of_birth)
        }


class Vehicle(models.Model):
    is_active = models.BooleanField(null=False, blank=False, default=True, db_index=True)

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
        return "%s : %s %s %s %s" % (self.id, self.year, self.make, self.model, self.style)


    def natural_key(self):
        return self.source_id, self.vin

    class Meta:
        unique_together = (('source_id', 'vin'),)