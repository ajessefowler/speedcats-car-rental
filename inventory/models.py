from django.db import models
from django.urls import reverse

class Store(models.Model):

	address = models.CharField(max_length=100)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=2)
	zipcode = models.IntegerField()
	phone = models.CharField(max_length=10)
	email = models.EmailField(max_length=254)
	
	def get_absolute_url(self):
		return reverse('store-detail-view', args=[str(self.id)])

	def __str__(self):
		return 'Store #' + str(self.id) + ', ' + self.address + ' ' + self.city + ', ' + self.state

class Vehicle(models.Model):

	VIN = models.CharField(max_length=17)
	store = models.ForeignKey(Store, on_delete=models.CASCADE)
	year = models.IntegerField()
	make = models.CharField(max_length=30)
	model = models.CharField(max_length=30)
	color = models.CharField(max_length=10)
	mileage = models.IntegerField()

	def get_absolute_url(self):
		return reverse('vehicle-detail-view', args=[str(self.id)])

	def __str__(self):
		return str(self.VIN) + ', ' + self.color + ' ' + str(self.year) + ' ' + self.make + ' ' + self.model + ', ' + str(self.mileage) + ' miles, ' + str(self.store)