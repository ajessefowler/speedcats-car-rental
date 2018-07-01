import json
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Store, Vehicle

def index(request):
	locations = Store.objects.all().values('address', 'city', 'state')
	locations_json = json.dumps(list(locations), cls=DjangoJSONEncoder)
	context = {
		"locations":locations_json
	}

	return render(request, 'inventory/index.html', context)
	
def faqs(request):
	return render(request, 'inventory/faqs.html')

def contact(request):
	return render(request, 'inventory/contact.html')

def feedback(request):
	return render(request, 'inventory/feedback.html')

def store(request, storeID):
	vehicles = Vehicle.objects.filter(store_id=storeID).filter(status='a')
	context = {
		"vehicles":vehicles
	}
	return render(request, 'inventory/vehicle_list.html', context)

def vehicle(request, storeID, vehicleID):
	vehicle = get_object_or_404(Vehicle, pk=vehicleID)
	context = {
		"vehicle":vehicle
	}
	return render(request, 'inventory/vehicle_detail.html', context)

def reserve(request, storeID, vehicleID):
	vehicle = get_object_or_404(Vehicle, pk=vehicleID)
	context = {
		"vehicle":vehicle
	}
	return render(request, 'inventory/reserve_vehicle.html', context)