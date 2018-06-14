from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('<int:storeID>/', views.store, name='store'),
	path('<int:storeID>/<int:vehicleID>/', views.vehicle, name='vehicle')
]