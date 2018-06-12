import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.http import HttpResponse
from .models import Store, Vehicle

def index(request):
	locations = Store.objects.all().values('address', 'city', 'state')
	locations_json = json.dumps(list(locations), cls=DjangoJSONEncoder)
	context = {
		"locations":locations_json
	}

	return render(request, 'inventory/index.html', context)

def store(request, storeID):
	vehicles = Vehicle.objects.filter(store_id=storeID)
	context = {
		"vehicles":vehicles
	}
	return render(request, 'inventory/vehicle_list.html', context)