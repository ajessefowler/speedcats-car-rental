from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator

import pytz
import datetime
#from celery import Celery
#from speedcats.celery_tasks import set_vehicle_as_reserved, set_vehicle_as_available
'''
# Profile extension found here: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	# Phone regex found here: https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
	address = models.CharField(max_length=100)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=2)
	zipcode = models.IntegerField()
	license_state = models.CharField(max_length=2)

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()
'''
class Store(models.Model):

	ID = models.IntegerField(primary_key=True)
	address = models.CharField(max_length=100)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=2)
	zipcode = models.IntegerField()
	phone = models.CharField(max_length=10)
	email = models.EmailField(max_length=254)
	
	def get_absolute_url(self):
		return reverse('store-detail-view', args=[str(self.StoreID)])

	def __str__(self):
		return self.address + ', ' + self.city + ', ' + self.state

class Vehicle(models.Model):

	status_choices = (
		('m', 'Maintenance'),
		('a', 'Available'),
		('r', 'Reserved'),
	)

	vehicle_type_choices = (
		('c', 'Car'),
		('s', 'SUV'),
		('t', 'Truck'),
	)

	engine_type_choices = (
		('i4', 'Inline 4'),
		('i6', 'Inline 6'),
		('v4', 'V4'),
		('v6', 'V6'),
		('v8', 'V8'),
		('w8', 'W8'),
		('vr6', 'VR6'),
		('e', 'Electric'),
		('h', 'Hybrid'),
	)

	VIN = models.CharField(max_length=17)
	store = models.ForeignKey(Store, on_delete=models.CASCADE)
	year = models.IntegerField()
	make = models.CharField(max_length=30)
	model = models.CharField(max_length=30)
	color = models.CharField(max_length=10)
	mileage = models.IntegerField()
	image = models.ImageField(upload_to="vehicle_photos", blank=True)
	gas_mileage = models.IntegerField(null=True, blank=True)
	engine_size = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
	engine_type = models.CharField(
		max_length=3,
		choices=engine_type_choices,
		default='i4',
	)
	storage_space = models.IntegerField(null=True, blank=True)
	horsepower = models.IntegerField(null=True, blank=True)
	price = models.DecimalField(max_digits=8, decimal_places=2, default=85.99)
	status = models.CharField(
		max_length=1,
		choices=status_choices,
		default='a',
	)
	vehicle_type = models.CharField(
		max_length=1,
		choices=vehicle_type_choices,
		default='c',
	)

	def get_absolute_url(self):
		return reverse('vehicle-detail-view', args=[str(self.id)])

	def __str__(self):
		return str(self.year) + ' ' + self.make + ' ' + self.model

class Reservation(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations")
	vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
	pick_up_time = models.DateTimeField(blank=False, null=False)
	pick_up_location = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='pick_up_store')
	drop_off_time = models.DateTimeField(blank=False, null=False)
	drop_off_location = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='drop_off_store')
	subtotal = models.DecimalField(max_digits=8, decimal_places=2, null=True)
	tax = models.DecimalField(max_digits=8, decimal_places=2, null=True)
	total = models.DecimalField(max_digits=8, decimal_places=2, null=True)
	miles_driven = models.IntegerField(null=True, blank=True)
	
	@property
	def status(self):
		pick_up_time = self.pick_up_time
		drop_off_time = self.drop_off_time
		now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)

		if pick_up_time > now:
			return 'Upcoming'
		elif drop_off_time > now:
			return 'In Progress'
		elif now > drop_off_time:
			return 'Completed'

	@property
	def length(self):
		pick_up_time = self.pick_up_time
		drop_off_time = self.drop_off_time
		length = drop_off_time - pick_up_time
		return (int(length.days) + 1)

	def __str__(self):
		return str(self.vehicle) + ' ' + str(self.pick_up_time)[:10] + ' to ' + str(self.drop_off_time)[:10]
'''
	# Create tasks to update vehicle status and store at pick up and drop off times
	def save(self, *args, **kwargs):
		create_task = False

		if self.pk is None:
			create_task = True

		super(Reservation, self).save(*args, **kwargs)

		if create_task:
			set_vehicle_as_reserved.apply_async(args=[self.vehicle], eta=self.pick_up_time)
			set_vehicle_as_available.apply_async(args=[self.vehicle, self.drop_off_location], eta=self.drop_off_time)
		else:
			# remove current tasks, create new tasks for modification
			pass
'''
class Maintenance(models.Model):
	vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
	mechanic = models.CharField(max_length=100, default="")
	description = models.CharField(max_length=200, default="")
	date = models.DateTimeField(blank=False, null=False)
	price = models.DecimalField(max_digits=8, decimal_places=2, null=True)

	def __str__(self):
		return str(self.vehicle) + ' on ' + str(self.date)[:10]

class Payment(models.Model):
	payment_type_choices = (
		('i', 'In Store'),
		('v', 'Visa'),
		('m', 'Mastercard'),
		('d', 'Discover'),
		('a', 'American Express'),
	)

	reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
	amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
	date = models.DateTimeField(blank=False, null=False)
	payment_type = models.CharField(
		max_length=1,
		choices=payment_type_choices,
		default='i',
	) 
