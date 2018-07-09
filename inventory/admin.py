from django.contrib import admin
from .models import Profile, Store, Vehicle, Reservation

admin.site.register(Profile)
admin.site.register(Store)
admin.site.register(Vehicle)
admin.site.register(Reservation)
