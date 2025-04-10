from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
import datetime
from django.views import View
from accidents.models import Accident, Authority
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import date
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'Authority/index.html'
    login_url = '/'

class AddAccident(TemplateView):
    template_name = 'Authority/add_accident.html'

    
    def post(self, request, *args, **kwargs):
        district = request.POST['district']
        police_station = request.POST['police_station']
        location = request.POST['location']
        road_name = request.POST['road_name']
        latitude = float(request.POST['latitude'])
        longitude = float(request.POST['longitude'])
        fatality=request.POST['fatality']

        # Create accident record
        accident, created = Accident.objects.get_or_create(
            district=district,
            police_station=police_station,
            location=location,
            road_name=road_name,
            latitude=latitude,
            longitude=longitude,
        )

        # Increment accident count
        accident.total_accidents += 1

        # Increment fatality count if fatality is "yes"
        if fatality.lower() == "yes":
            accident.total_fatalities += 1

        accident.save()
        messages = "Accident Data Added Successfull"
        return render(request, 'Authority/index.html', {'message': messages})


class ViewAccident(LoginRequiredMixin, TemplateView):
    template_name = 'Authority/view_accident.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ViewAccident, self).get_context_data(**kwargs)
        com = (
            Accident.objects.values("district", "police_station", "location", "road_name", "latitude", "longitude")
            .annotate(total_accidents=Sum("total_accidents"), total_fatalities=Sum("total_fatalities"))
            .order_by("district", "police_station", "location")  # Order by location
        )
        context['com'] = com
        return context


class DeleteAccident(View):
   def dispatch(self, request, *args, **kwargs):
        accident_id= request.GET['id']
        accident= get_object_or_404(Accident, id=accident_id)
        accident.delete()
        return render(request, 'Authority/view_accident.html', {'message': "Accident Data Deleted successfully"})

