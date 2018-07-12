from django.urls import path

from . import views

app_name = 'inventory'
urlpatterns = [
	path('', views.index, name='index'),
	path('register/', views.register, name='register'),
	path('faqs/', views.faqs, name='faqs'),
	path('home/', views.home, name='home'),
	path('history/', views.history, name="history"),
	path('contact/', views.contact, name='contact'),
	path('feedback/', views.feedback, name='feedback'),
	path('reservation/<int:reservationID>/modify/', views.modify, name='modify'),
	path('reservation/<int:reservationID>/update/', views.update, name='update'),
	path('reservation/<int:reservationID>/cancel/', views.cancel, name='cancel'),
	path('reservation/<int:reservationID>', views.reservation, name='reservation'),
	path('locations/', views.locations, name='locations'),
	path('vehicles/', views.store, name='store'),
	path('vehicles/search/', views.search, name='search'),
	path('<int:storeID>/<int:vehicleID>/', views.vehicle, name='vehicle'),
	path('<int:storeID>/<int:vehicleID>/reserve/', views.reserve, name='reserve'),
	path('<int:storeID>/<int:vehicleID>/reserve/confirm/', views.makereservation, name='makereservation')
]