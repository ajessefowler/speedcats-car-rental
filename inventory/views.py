import json
import pytz
from datetime import datetime, timedelta
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db import transaction
from django.db.models.signals import post_save
from django.db.models import Q
from django.dispatch import receiver
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from .tokens import account_activation_token
from .forms import RegisterForm, ProfileForm
from .models import Store, Vehicle, Reservation, Payment

def home(request):
	# Pass location data so front-end map can display store markers
	locations = Store.objects.all().values('address', 'city', 'state')
	locations_json = json.dumps(list(locations), cls=DjangoJSONEncoder)
	
	context = {
		"locations":locations_json
	}

	return render(request, 'inventory/home.html', context)
	
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
		register_form = RegisterForm(request.POST)
		profile_form = ProfileForm(request.POST)
		if register_form.is_valid() and profile_form.is_valid():
			user = register_form.save(commit=False)
			user.is_active = False
			user.save()
			current_site = get_current_site(request)
			subject = 'Activate Your Speedcats Car Rental Account'
			message = render_to_string('account_activation_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
				'token': account_activation_token.make_token(user),
			})
			user.email_user(subject, message)
			return redirect('inventory:account_activation_sent')

	else:
		register_form = RegisterForm()
		profile_form = ProfileForm()

	context = {
		"register_form":register_form,
		"profile_form":profile_form
	}
	return render(request, 'inventory/register.html', context)

def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user:
		print(user.first_name)
	
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.profile.email_confirmed = True
		user.save()
		login(request, user)
		return redirect('/')
	else:
		 return render(request, 'account_activation_invalid.html')

def account_activation_sent(request):
	return render(request, 'account_activation_sent.html')

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
	paginator = Paginator(available_vehicles, 10)

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

	# Split query into words and filter selected store for available vehicles with first word
	search_terms = query.split()
	results = Vehicle.objects.filter(store_id=pickup_id).filter(status='a').filter(Q(year__icontains=search_terms[0]) | Q(make__icontains=search_terms[0]) | Q(model__icontains=search_terms[0]) | Q(color__icontains=search_terms[0]))

	# If query has more than 1 word, filter results with each word
	if len(search_terms) > 1:
		for term in search_terms[1:]:
			results = results.filter(Q(year__icontains=term) | Q(make__icontains=term) | Q(model__icontains=term) | Q(color__icontains=term))

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
			dropoff_store = get_object_or_404(Store, pk=dropoff_id)
			vehicle = get_object_or_404(Vehicle, pk=vehicleID)
		except KeyError:
			raise Http404('Store does not exist')
		except Store.DoesNotExist:
			raise Http404('Store does not exist')
	else:
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
		payment_type = request.POST["paymenttype"]
	except KeyError:
		pass

	now = datetime.now()
	
	# Create new reservation
	reservation = Reservation(user=user, vehicle=vehicle, pick_up_time=pickup_time, pick_up_location=pickup_store, drop_off_time=dropoff_time, drop_off_location=dropoff_store, subtotal=subtotal, tax=tax, total=total)
	reservation.save()

	# Create new payment
	payment = Payment(reservation=reservation, amount=total, date=now, payment_type=payment_type)
	payment.save()

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

		subtotal = request.POST["subtotal"]
		tax = request.POST["tax"]
		total = request.POST["total"]

		reservation.subtotal = subtotal
		reservation.tax = tax
		reservation.total = total

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

@login_required
def change_pick_up(request, storeID, vehicleID):
	user = request.user
	store = get_object_or_404(Store, pk=storeID)
	vehicle = get_object_or_404(Vehicle, pk=vehicleID)
	pickup_id = request.session["pickup_id"]
	pickup_time = request.session["pickup_time"]
	dropoff_id = request.session["dropoff_id"]
	dropoff_store = get_object_or_404(Store, pk=dropoff_id)
	dropoff_time = request.session["dropoff_time"]

	pickup_format = datetime.strptime(pickup_time, "%Y-%m-%d %H:%M")
	dropoff_format = datetime.strptime(dropoff_time, "%Y-%m-%d %H:%M")

	context = {
		"store":store,
		"drop_off_store":dropoff_store,
		"pick_up_time":pickup_time,
		"pick_up_format":pickup_format,
		"drop_off_time":dropoff_time,
		"drop_off_format":dropoff_format,
		"vehicle":vehicle
	}

	return render(request, 'inventory/change_pick_up.html', context)

@login_required
def change_drop_off(request, storeID, vehicleID):
	user = request.user
	store = get_object_or_404(Store, pk=storeID)
	vehicle = get_object_or_404(Vehicle, pk=vehicleID)
	pickup_id = request.session["pickup_id"]
	pickup_time = request.session["pickup_time"]
	dropoff_id = request.session["dropoff_id"]
	dropoff_store = get_object_or_404(Store, pk=dropoff_id)
	dropoff_time = request.session["dropoff_time"]

	pickup_format = datetime.strptime(pickup_time, "%Y-%m-%d %H:%M")
	dropoff_format = datetime.strptime(dropoff_time, "%Y-%m-%d %H:%M")

	context = {
		"store":store,
		"drop_off_store":dropoff_store,
		"pick_up_time":pickup_time,
		"pick_up_format":pickup_format,
		"drop_off_time":dropoff_time,
		"drop_off_format":dropoff_format,
		"vehicle":vehicle
	}

	return render(request, 'inventory/change_drop_off.html', context)