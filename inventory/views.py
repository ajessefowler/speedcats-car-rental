import json
import pytz
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Store, Vehicle, Reservation

def home(request):
	return render(request, 'inventory/home.html')
	
def faqs(request):
	return render(request, 'inventory/faqs.html')

def contact(request):
	return render(request, 'inventory/contact.html')

def feedback(request):
	return render(request, 'inventory/feedback.html')

def locations(request):
	return render(request, 'inventory/locations.html')

def index(request):
	# Pass location data so front-end map can display store markers
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

	available_vehicles = []
	store = Store.objects.get(pk=pickup_id)
	vehicles = Vehicle.objects.filter(store_id=pickup_id).filter(status='a')

	pickup_format = datetime.strptime(pickup_time, "%Y-%m-%d %H:%M").replace(tzinfo=pytz.UTC)
	dropoff_format = datetime.strptime(dropoff_time, "%Y-%m-%d %H:%M").replace(tzinfo=pytz.UTC)

	# Check if vehicle is available during entire reservation time
	for vehicle in vehicles:
		if len(vehicle.reservation_set.all()) == 0:
			available_vehicles.append(vehicle)
		else:
			for reservation in vehicle.reservation_set.all():
				if reservation.drop_off_time < pickup_format or reservation.pick_up_time > dropoff_format:
					available_vehicles.append(vehicle)
			
	context = {
		"vehicles":available_vehicles,
		"store":store
	}

	return render(request, 'inventory/vehicle_list.html', context)

def search(request):
	query = request.POST["searchquery"]
	results = Vehicle.objects.annotate(
		search=SearchVector('year', 'make', 'model', 'color'),
	).filter(search=query)

	context = {
		"results":results
	}

	return render(request, 'inventory/search.html', context)


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

	# Calculate the length of the potential reservation, rounding number of days up
	dropoff_format = datetime.strptime(request.session["dropoff_time"], "%Y-%m-%d %H:%M").replace(tzinfo=pytz.UTC)
	pickup_format = datetime.strptime(request.session["pickup_time"], "%Y-%m-%d %H:%M").replace(tzinfo=pytz.UTC)
	reservation_length = ((dropoff_format - pickup_format) + timedelta(days=1)).days + 1

	# Calculate pricing of potential reservation
	subtotal = vehicle.price * reservation_length
	tax = round(float(subtotal) * 0.07,2)
	total = round(float(subtotal) + tax,2)
	
	context = {
		"store":store,
		"vehicle":vehicle,
		"length":reservation_length,
		"subtotal":subtotal,
		"tax":tax,
		"total":total
	}
	return render(request, 'inventory/reserve_vehicle.html', context)

@login_required
def makereservation(request, storeID, vehicleID):
	try:
		user = request.user
		vehicle = Vehicle.objects.get(pk=vehicleID)
		pickup_id = request.session["pickup_id"]
		pickup_store = get_object_or_404(Store, pk=pickup_id)
		pickup_time = request.session["pickup_time"]
		dropoff_id = request.session["dropoff_id"]
		dropoff_store = get_object_or_404(Store, pk=dropoff_id)
		dropoff_time = request.session["dropoff_time"]
	except KeyError:
		pass
	
	# Create new reservation
	reservation = Reservation(user=user, vehicle=vehicle, pick_up_time=pickup_time, pick_up_location=pickup_store, drop_off_time=dropoff_time, drop_off_location=dropoff_store)
	reservation.save()

	context = {
		"reservation":reservation
	}
	return render(request, 'inventory/confirm.html', context)

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
	if user == reservation.user:
		reservation = Reservation.objects.get(pk=reservationID)
		reservation.vehicle.status = 'a'
		reservation.vehicle.save()
		reservation.delete()
		reservations = Reservation.objects.filter(user=user)
	context = {
		"reservations":reservations
	}
	return render(request, 'inventory/history.html', context)