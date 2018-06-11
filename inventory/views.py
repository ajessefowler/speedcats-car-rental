import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from .models import Store, Vehicle

def index(request):
	locations = Store.objects.all().values('address', 'city', 'state')
	locations_json = json.dumps(list(locations), cls=DjangoJSONEncoder)

	return render(request, 'inventory/index.html', {'locations':locations_json})

class StoreVehicles(generic.ListView):
	model = Vehicle
	paginate_by = 20
	template_name = 'inventory/vehicles_list.html'