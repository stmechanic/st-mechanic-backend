from django.contrib import admin

from .models import Garage, Vehicle, Job, Rating, Quote, Mechanic, Payment

admin.site.register(Garage)
admin.site.register(Vehicle)
admin.site.register(Job)
admin.site.register(Rating)
admin.site.register(Quote)
admin.site.register(Mechanic)
admin.site.register(Payment)

