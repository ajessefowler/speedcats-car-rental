from django.contrib import admin
from .models import Store, Vehicle, Reservation, Maintenance

class StoreAdmin(admin.ModelAdmin):
    list_display = ('address', 'city', 'state', 'zipcode', 'phone', 'email')
    list_filter = ['city', 'state']

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'color', 'mileage', 'VIN', 'vehicle_type', 'status', 'price')
    list_filter = ['status', 'vehicle_type']
    search_fields = ['VIN', 'year', 'make', 'model', 'color']

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'user', 'pick_up_time', 'pick_up_location', 'drop_off_time', 'drop_off_location')
    list_filter = ['pick_up_time', 'pick_up_location__city', 'drop_off_time', 'drop_off_location__city']
    search_fields = ['vehicle__year', 'vehicle__make', 'vehicle__model', 'user__username', 'user__first_name', 'user__last_name']

#admin.site.register(Profile)
admin.site.register(Store, StoreAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Maintenance)
