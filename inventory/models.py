from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver

import pytz
import datetime

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
		('l', 'Loaned'),
		('a', 'Available'),
		('r', 'Reserved'),
	)

	vehicle_type_choices = (
		('c', 'Car'),
		('s', 'SUV'),
		('t', 'Truck'),
	)

	VIN = models.CharField(max_length=17)
	store = models.ForeignKey(Store, on_delete=models.CASCADE)
	year = models.IntegerField()
	make = models.CharField(max_length=30)
	model = models.CharField(max_length=30)
	color = models.CharField(max_length=10)
	mileage = models.IntegerField()
	image = models.ImageField(upload_to="vehicle_photos", blank=True)
	description = models.CharField(max_length=800, default="")
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
	
	"""
	@property
	def active(self):
		now = datetime.datetime.utcnow()
		if self.pick_up_time < now and now < self.drop_off_time:
			return True
		return False
	"""

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