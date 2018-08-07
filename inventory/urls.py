from django.urls import path

from . import views

app_name = 'inventory'
urlpatterns = [
	path('', views.index, name='index'),
	path('documents/', views.documents, name='documents'),
	path('training/', views.training, name='training'),
	path('accounting/', views.accounting, name='accounting'),
	path('marketing/', views.marketing, name='marketing'),
	path('daily_summary/', views.daily_summary, name='daily_summary'),
	path('daily_sales/', views.daily_sales, name='daily_sales'),
	path('hourly_detail/', views.hourly_detail, name='hourly_detail'),
	path('weekly_sales/', views.weekly_sales, name='weekly_sales'),
	path('weekly_maintenance/', views.weekly_maintenance, name='weekly_maintenance'),
	path('register/', views.register, name='register'),
	path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
	path('activate/<uidb64>/<token>/', views.activate, name='activate'),
	path('faqs/', views.faqs, name='faqs'),
	path('home/', views.home, name='home'),
	path('history/', views.history, name='history'),
	path('contact/', views.contact, name='contact'),
	path('feedback/', views.feedback, name='feedback'),
	path('reservation/<int:reservationID>/modify/', views.modify, name='modify'),
	path('reservation/<int:reservationID>/update/', views.update, name='update'),
	path('reservation/<int:reservationID>/cancel/', views.cancel, name='cancel'),
	path('reservation/<int:reservationID>', views.reservation, name='reservation'),
	path('locations/', views.locations, name='locations'),
	path('vehicles/', views.store, name='store'),
	path('vehicles/(?P<page>[a-z0-9]+)/$', views.store, name='storepage'),
	path('vehicles/search/', views.search, name='search'),
	path('<int:storeID>/<int:vehicleID>/', views.vehicle, name='vehicle'),
	path('<int:storeID>/<int:vehicleID>/reserve/', views.reserve, name='reserve'),
	path('<int:storeID>/<int:vehicleID>/reserve/changepickup/', views.change_pick_up, name='change_pick_up'),
	path('<int:storeID>/<int:vehicleID>/reserve/changedropoff/', views.change_drop_off, name='change_drop_off'),
	path('<int:storeID>/<int:vehicleID>/reserve/confirm/', views.makereservation, name='makereservation')
]