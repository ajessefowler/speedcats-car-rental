from django.db import models
from django.urls import reverse

class Store(models.Model):

	ID = models.IntegerField(primary_key=True, unique=True, default=0)
	address = models.CharField(max_length=100)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=2)
	zipcode = models.IntegerField()
	phone = models.CharField(max_length=10)
	email = models.EmailField(max_length=254)
	
	def get_absolute_url(self):
		return reverse('store-detail-view', args=[str(self.StoreID)])

	def __str__(self):
		return 'Store #' + str(self.ID) + ', ' + self.address + ' ' + self.city + ', ' + self.state

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