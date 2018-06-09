from django.shortcuts import render
from django.http import HttpResponse
from .models import Store, Vehicle

def index(request):
	num_vehicles = Vehicle.objects.all().count()

	return render(
		request,
		'index.html',
		context={'num_vehicles':num_vehicles},
	)
