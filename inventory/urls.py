from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('store/<int:storeID>/', views.StoreVehicles.as_view(), name='storevehicles'),
]