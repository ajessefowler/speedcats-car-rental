import json
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Store, Vehicle, Reservation

def index(request):
	locations = Store.objects.all().values('address', 'city', 'state')
	locations_json = json.dumps(list(locations), cls=DjangoJSONEncoder)
	context = {
		"locations":locations_json
	}

	return render(request, 'inventory/index.html', context)
	
@login_required
def history(request):
	user = request.user
	reservations = Reservation.objects.filter(user=user)
	context = {
		"reservations":reservations
	}

	return render(request, 'inventory/history.html', context)

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

@login_required
def reserve(request, storeID, vehicleID):
	store = get_object_or_404(Store, pk=storeID)
	vehicle = get_object_or_404(Vehicle, pk=vehicleID)
	context = {
		"store":store,
		"vehicle":vehicle
	}
	return render(request, 'inventory/reserve_vehicle.html', context)

@login_required
def makereservation(request, storeID, vehicleID):
	try:
		user = request.user
		vehicle = Vehicle.objects.get(pk=vehicleID)
		pickup_id = int(request.POST["pickupstore"])
		pickup_store = get_object_or_404(Store, pk=pickup_id)
		pickup_time = request.POST["pickuptime"]
		dropoff_id = int(request.POST["dropoffstore"])
		dropoff_store = get_object_or_404(Store, pk=dropoff_id)
		dropoff_time = request.POST["dropofftime"]
	except KeyError:
		pass
	reservation = Reservation(user=user, vehicle=vehicle, pick_up_time=pickup_time, pick_up_location=pickup_store, drop_off_time=dropoff_time, drop_off_location=dropoff_store)
	reservation.save()
	return HttpResponseRedirect('/')