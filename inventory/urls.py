from django.urls import path

from . import views

app_name = 'inventory'
urlpatterns = [
	path('', views.index, name='index'),
	path('faqs/', views.faqs, name='faqs'),
	path('history/', views.history, name="history"),
	path('contact/', views.contact, name='contact'),
	path('feedback/', views.feedback, name='feedback'),
	path('<int:storeID>/', views.store, name='store'),
	path('<int:storeID>/<int:vehicleID>/', views.vehicle, name='vehicle'),
	path('<int:storeID>/<int:vehicleID>/reserve/', views.reserve, name='reserve'),
	path('<int:storeID>/<int:vehicleID>/reserve/confirm/', views.makereservation, name='makereservation')
]