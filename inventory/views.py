import json
import pytz
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Store, Vehicle, Reservation

def index(request):
	locations = Store.objects.all().values('address', 'city', 'state')
	locations_json = json.dumps(list(locations), cls=DjangoJSONEncoder)
	context = {
		"locations":locations_json
	}

	return render(request, 'inventory/index.html', context)
	
def home(request):
	return render(request, 'inventory/home.html')

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

def store(request):
	try:
		pickup_id = int(request.POST["pickuplocationid"])
		pickup_time = request.POST["pickuptimeformat"]
		dropoff_id = int(request.POST["dropofflocationid"])
		dropoff_time = request.POST["dropofftimeformat"]
		request.session["pickup_id"] = pickup_id
		request.session["pickup_time"] = pickup_time
		request.session["dropoff_id"] = dropoff_id
		request.session["dropoff_time"] = dropoff_time
	except KeyError:
		pass

	dropoff_format = datetime.strptime(dropoff_time, "%Y-%m-%d %H:%M").utcnow().replace(tzinfo=pytz.UTC)
	available_vehicles = []
	store = Store.objects.get(pk=pickup_id)
	vehicles = Vehicle.objects.filter(store_id=pickup_id).filter(status='a')

	# Check if vehicle is available during entire reservation time
	for vehicle in vehicles:
		if len(vehicle.reservation_set.all()) == 0:
			available_vehicles.append(vehicle)
		else:
			for reservation in vehicle.reservation_set.all():
				if reservation.pick_up_time < dropoff_format:
					available_vehicles.append(vehicle)
			
	context = {
		"vehicles":available_vehicles,
		"store":store
	}

	return render(request, 'inventory/vehicle_list.html', context)

def vehicle(request, storeID, vehicleID):
	vehicle = get_object_or_404(Vehicle, pk=vehicleID)
	reservations = vehicle.reservation_set
	context = {
		"vehicle":vehicle,
		"reservations":reservations
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

@login_required
def reservation(request, reservationID):
	reservation = Reservation.objects.get(pk=reservationID)
	context = {
		"reservation":reservation
	}

	# If user made the reservation, display details, otherwise display error
	if request.user == reservation.user:
		return render(request, 'inventory/reservation.html', context)

@login_required
def modify(request, reservationID):
	reservation = Reservation.objects.get(pk=reservationID)
	context = {
		"reservation":reservation
	}
	if request.user == reservation.user:
		return render(request, 'inventory/modify.html', context)

@login_required
def cancel(request, reservationID):
	user = request.user
	reservation = Reservation.objects.get(pk=reservationID)
	reservation.vehicle.status = 'a'
	reservation.vehicle.save()
	reservation.delete()
	reservations = Reservation.objects.filter(user=user)
	context = {
		"reservations":reservations
	}
	return render(request, 'inventory/history.html', context)