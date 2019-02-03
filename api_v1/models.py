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
    proto_class = vehicle_pb2.Vehicle

    objects = VehicleManager()
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

    def __unicode__(self):
        return "%s : %s %s %s %s" % (self.id, self.year, self.make, self.model, self.style)

    @classmethod
    def get_by_id(cls, vehicle_id):
        return cls._get_queryset_get_job().get(pk=vehicle_id)

    @classmethod
    def _get_queryset_get_job(cls):
        return InfiniteQuerySetGetJob(Vehicle, lifetime=settings.CACHE_LIFETIME_CARRIER,
                                      tags=(settings.CACHE_TAGS['VEHICLE_QUERYSET'],))

    @classmethod
    def get_years(cls):
        return cls._get_values_list_filter_job(values=('year',), order_by=('-year',), return_json=False).get()

    @classmethod
    def get_makes_for_year(cls, year, return_json=False):
        return get_vehicle_json_info(select_values=('make',), order_by=('make',),
                                     query_filter=(('year', year), ('is_active', True),),
                                     selected_vehicle=str(year), return_json=return_json)

    @classmethod
    def get_models_for_make(cls, year, make, return_json=False):
        return get_vehicle_json_info(select_values=('model',), order_by=('model',),
                                     query_filter=(('year', year), ('make', make), ('is_active', True),),
                                     selected_vehicle='{0} {1}'.format(year, make), return_json=return_json)

    @classmethod
    def get_by_vin_startswith_match(cls, vin, return_json):
        return cls._get_values_list_filter_job(
            values=('id', 'year', 'make', 'model', 'style', 'vin'),
            order_by=('source_id', '-msrp'),
            return_json=return_json,
            distinct_on=('source_id',)).get(vin__startswith=str(vin).upper(), is_active=True)

    @classmethod
    def get_by_vin(cls, vin, return_json):
        return cls._get_values_list_filter_job(
            values=('id', 'year', 'make', 'model', 'style'),
            order_by=('source_id', '-msrp'),
            return_json=return_json,
            distinct_on=('source_id',)).get(vin=vin, is_active=True)

    @classmethod
    def get_first_vehicle_id_by_vin_or_year_make_model(cls, vin, year, make, model):
        vehicle_id = cls.get_first_vehicle_id_by_vin(vin)
        if vehicle_id:
            return vehicle_id
        return cls.get_first_vehicle_id_for_model(year, make, model)

    @classmethod
    def get_first_vehicle_id_by_vin(cls, vin):
        vehicle = cls.get_by_vin(vin, False)
        if vehicle:
            return vehicle[0][0]
        return None  # for clarity

    @classmethod
    def get_first_vehicle_id_for_model(cls, year, make, model):
        result = SearchQuerySet().using(settings.VEHICLE_INDEX) \
            .models(Vehicle) \
            .autocomplete(vehicle_display_name="%s %s %s" % (year, make, model)) \
            .values('vehicle_id', 'vehicle_display_name')
        if result and result[0]:
            return result[0]['vehicle_id']
        return None  # for clarity

    @classmethod
    def get_vehicle_id_closest_match_for_model(cls, year, make, model):
        results = SearchQuerySet().using(settings.VEHICLE_INDEX) \
            .models(Vehicle) \
            .autocomplete(vehicle_display_name="%s %s %s" % (year, make, model)) \
            .values('vehicle_id', 'vehicle_display_name')
        # Let's get the closest match on year/make
        for result in results:
            display_name = result['vehicle_display_name']
            if year in display_name and make.lower() in display_name.lower():
                return result['vehicle_id']
        return None  # for clarity

    @classmethod
    def get_vehicle_id_base_model_for_model(cls, year, make, model):
        results = get_vehicle_json_info(
            select_values=('id', 'style', 'source_id', 'vin'),
            # order by msrp desc to match VehicleIndex (haystack search index)
            order_by=('source_id', '-msrp'),
            distinct_on=('source_id',),
            query_filter=(('year', year),
                          ('make', make),
                          ('model', model),
                          ('is_active', True)),
            selected_vehicle='{0} {1} {2}'.format(year, make, model),
            return_json=False
        )
        if results and results[0]:
            return results[0][0]
        return None  # for clarity

    @classmethod
    def get_submodels_for_model(cls, year, make, model, return_json=False):
        return get_vehicle_json_info(
            select_values=('id', 'style', 'source_id', 'vin'),
            # order by msrp desc to match VehicleIndex (haystack search index)
            order_by=('style', 'source_id', '-msrp'),
            distinct_on=('style', 'source_id',),
            query_filter=(('year', year),
                          ('make', make),
                          ('model', model),
                          ('is_active', True)),
            selected_vehicle='{0} {1} {2}'.format(year, make, model),
            return_json=return_json
        )

    @classmethod
    def _get_values_list_filter_job(cls, values, order_by, return_json, distinct_on=()):
        return InfiniteQuerySetFilterValuesListJob(Vehicle, lifetime=settings.CACHE_LIFETIME_VEHICLE,
                                                   tags=(settings.CACHE_TAGS['VEHICLE_QUERYSET'],),
                                                   select_values=values,
                                                   order_by=order_by,
                                                   return_json=return_json,
                                                   distinct_on=distinct_on)

    def natural_key(self):
        return self.source_id, self.vin

    class Meta:
        unique_together = (('source_id', 'vin'),)