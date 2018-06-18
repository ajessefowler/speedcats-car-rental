from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('login/', views.login, name='login'),
	path('faqs/', views.faqs, name='faqs'),
	path('contact/', views.contact, name='contact'),
	path('feedback/', views.feedback, name='feedback'),
	path('<int:storeID>/', views.store, name='store'),
	path('<int:storeID>/<int:vehicleID>/', views.vehicle, name='vehicle'),
	path('<int:storeID>/<int:vehicleID>/reserve/', views.reserve, name='reserve')
]