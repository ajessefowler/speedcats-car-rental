import json
import pytz
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.postgres.search import SearchVector
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models.signals import post_save
from django.db.models import Q
from django.dispatch import receiver
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import RegisterForm
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
	locations = Store.objects.all()

	context = {
		"locations":locations
	}

	return render(request, 'inventory/locations.html', context)

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('/')
	else:
		form = RegisterForm()

	context = {
		"form":form
	}
	return render(request, 'inventory/register.html', context)

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

	# If data is being posted, use that, otherwise use the session variables
	if request.method == "POST":
		try:
			pickup_id = int(request.POST["pickuplocationid"])
			pickup_time = request.POST["pickuptimeformat"]
			dropoff_id = int(request.POST["dropofflocationid"])
			dropoff_time = request.POST["dropofftimeformat"]

			request.session["pickup_id"] = pickup_id
			request.session["pickup_time"] = pickup_time
			request.session["dropoff_id"] = dropoff_id
			request.session["dropoff_time"] = dropoff_time

			store = Store.objects.get(pk=pickup_id)
		except KeyError:
			raise Http404('Store does not exist')
		except Store.DoesNotExist:
			raise Http404('Store does not exist')
	else:
		pickup_id = request.session["pickup_id"]
		pickup_time = request.session["pickup_time"]
		dropoff_id = request.session["dropoff_id"]
		dropoff_time = request.session["dropoff_time"]

		store = Store.objects.get(pk=pickup_id)

	available_vehicles = []
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
	
	# Setup paginator to split up vehicles
	page = request.GET.get('page')
	paginator = Paginator(available_vehicles, 15)

	try:
		final_vehicles = paginator.page(page)
	except PageNotAnInteger:
		final_vehicles = paginator.page(1)
	except EmptyPage:
		final_vehicles = paginator.page(paginator.num_pages)

	context = {
		"vehicles":final_vehicles,
		"store":store
	}

	return render(request, 'inventory/vehicle_list.html', context)

def search(request):
	pickup_id = request.session["pickup_id"]
	store = Store.objects.get(pk=pickup_id)
	
	query = request.POST["searchquery"]
	results = Vehicle.objects.filter(store_id=pickup_id).filter(status='a').filter(Q(year__icontains=query) | Q(make__icontains=query) | Q(model__icontains=query) | Q(color__icontains=query))

	context = {
		"query":query,
		"results":results,
		"store":store
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

	dropoff_id = request.session["dropoff_id"]
	dropoff_store = get_object_or_404(Store, pk=dropoff_id)
	pickup_time = request.session["pickup_time"]
	dropoff_time = request.session["dropoff_time"]

	pickup_format = datetime.strptime(pickup_time, "%Y-%m-%d %H:%M")
	dropoff_format = datetime.strptime(dropoff_time, "%Y-%m-%d %H:%M")

	# Calculate the length of the potential reservation, rounding number of days up
	reservation_length = ((dropoff_format - pickup_format) + timedelta(days=1)).days

	# Calculate pricing of potential reservation
	subtotal = vehicle.price * reservation_length
	tax = round(float(subtotal) * 0.07,2)
	total = round(float(subtotal) + tax,2)
	
	context = {
		"store":store,
		"drop_off_store":dropoff_store,
		"pick_up_time":pickup_time,
		"pick_up_format":pickup_format,
		"drop_off_time":dropoff_time,
		"drop_off_format":dropoff_format,
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

		subtotal = request.POST["subtotal"]
		tax = request.POST["tax"]
		total = request.POST["total"]
	except KeyError:
		pass
	
	# Create new reservation
	reservation = Reservation(user=user, vehicle=vehicle, pick_up_time=pickup_time, pick_up_location=pickup_store, drop_off_time=dropoff_time, drop_off_location=dropoff_store, subtotal=subtotal, tax=tax, total=total)
	reservation.save()

	calc_drop_off = datetime.strptime(dropoff_time, "%Y-%m-%d %H:%M")
	calc_pick_up = datetime.strptime(pickup_time, "%Y-%m-%d %H:%M")
	length = int((calc_drop_off - calc_pick_up).days) + 1

	context = {
		"reservation":reservation,
		"length":length
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
	else:
		raise Http404('You do not have permission to view this page.')

@login_required
def modify(request, reservationID):
	reservation = Reservation.objects.get(pk=reservationID)
	context = {
		"reservation":reservation
	}
	if request.user == reservation.user:
		return render(request, 'inventory/modify.html', context)
	else:
		raise Http404('You do not have permission to view this page.')

@login_required
def update(request, reservationID):
	reservation = Reservation.objects.get(pk=reservationID)

	if request.user == reservation.user:
		if 'pickuplocationid' in request.POST:
			pickup_id = int(request.POST["pickuplocationid"])
			pickup_store = get_object_or_404(Store, pk=pickup_id)
			reservation.pick_up_location = pickup_store

		if 'pickuptimeformat' in request.POST:
			pickup_time = request.POST["pickuptimeformat"]
			pickup_format = datetime.strptime(pickup_time, "%Y-%m-%d %H:%M")
			reservation.pick_up_time = pickup_format

		dropoff_id = int(request.POST["dropofflocationid"])
		dropoff_store = get_object_or_404(Store, pk=dropoff_id)
		reservation.drop_off_location = dropoff_store

		dropoff_time = request.POST["dropofftimeformat"]
		dropoff_format = datetime.strptime(dropoff_time, "%Y-%m-%d %H:%M")
		reservation.drop_off_time = dropoff_format

		reservation.save()
		
		return redirect('/inventory/reservation/' + str(reservationID))
	else:
		raise Http404('You do not have permission to view this page.')

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