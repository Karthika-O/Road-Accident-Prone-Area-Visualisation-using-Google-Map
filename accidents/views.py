from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from accidents.models import Accident, Authority, UserType
from django.http import JsonResponse
from .models import Accident
import folium
from folium.plugins import HeatMap
import json

from django.contrib.auth import authenticate, login
# Create your views here.

class IndexView(TemplateView):
    template_name = 'index1.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        co = Authority.objects.filter(user__last_name='1')
        for co in co:
            st = co.id
            u = co.user.id

            j = Accident.objects.filter(id=st).count()
            print(j)
            if j >= 3:
                us = User.objects.get(pk=u)
                us.last_name = 0
                us.save()

            context['st'] = st

        return context
    
class AdminView(TemplateView):
    template_name = 'login.html'


class UserView(TemplateView):
    template_name = 'user.html'

    def get_contextsts(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(username=self.request.user)
        return context
    
class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if user.last_name == '1':
                if user.is_superuser:
                    return redirect('admin/')
                else:
                    return redirect('/Authority')
            else:
                return render(request, 'login.html', {'message': " User Account Not Authenticated"})
        else:
            return render(request, 'login.html', {'message': "Invalid Username or Password"})
        
class SignUp(TemplateView):
        template_name = 'SignUp.html'

class RegisterView(TemplateView):
    template_name = 'register.html'

    def post(self, request, *args, **kwargs):
        a='1967-1-1'
        b='2004-1-1'
        email = request.POST['email']
        fname = request.POST['pfirstna']
        lname = request.POST['plastna']
        gender = request.POST['pgender']
        dob = request.POST['pdob']
        print('cytfyt',dob)
        paddress = request.POST['pPermanantAddress']
        taddress = request.POST['pTemporaryAddress']
        phone = request.POST['pcontact']
        district = request.POST['pDistrict']
        badge_number = request.POST['pbadgeno']
        designation = request.POST['pdesign']
        jurisdiction = request.POST['pjuri']
        idprooof = request.FILES['pIDproof']
        photo = request.FILES['pPhoto']
        password = request.POST['password']
        if (dob>=a and dob<=b):

            try:

                u = User.objects.create_user(username=email, password=password, first_name=fname, last_name='1',
                                             email=email)
                u.save()

                w = Authority()
                w.user = u
                w.email=email
                w.pfirstna=fname
                w.plastna = lname
                w.pgender = gender
                w.pdob = dob
                w.pcontact = phone
                w.pDistrict = district
                w.pPermanantAddress = paddress
                w.pTemporaryAddress = taddress
                w.pdesign=designation
                w.pbadgeno= badge_number
                w.pjuri= jurisdiction
                w.pIDproof = idprooof
                w.pPhoto = photo
                w.count=0

                w.save()
                usertype = UserType()
                usertype.user = u
                usertype.type = 'Authority'
                usertype.save()

                messages = "Registration Successfull"
                return render(request, 'index.html', {'message': messages})
            except:
                messages = "Enter Another Username"
                return render(request, 'index.html', {'message': messages})
        else:
            messages = "Age is not Eligible"
            return render(request, 'index.html', {'message': messages})
        
def get_heatmap_data(request):
    # Fetch accident data
    accident_data = Accident.objects.all()

    # Ensure data is available
    if not accident_data:
        return render(request, "error.html", {"message": "No accident data available."})

    # Convert queryset to a list of tuples (latitude, longitude, severity_score)
    accident_list = [
        (accident.latitude, accident.longitude, accident.severity_score())
        for accident in accident_data
    ]

    # Compute average latitude and longitude for centering
    avg_lat = sum(lat for lat, lon, sev in accident_list) / len(accident_list)
    avg_lon = sum(lon for lat, lon, sev in accident_list) / len(accident_list)

    # Create a Folium map centered at the average location
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=10)

    # Add heatmap layer
    HeatMap(accident_list).add_to(m)

    # Save the generated map
    heatmap_path = "static/heatmap.html"
    m.save(heatmap_path)

    return render(request, "heatmap.html", {"map_path": heatmap_path})

def accident_map(request):
    accidents = Accident.objects.all()
    accident_data = [
        {
            "lat": a.latitude,
            "lng": a.longitude,
            "district": a.district,
            "police_station": a.police_station,
            "location": a.location,
            "road_name": a.road_name,
            "total_accidents": a.total_accidents,
            "total_fatalities": a.total_fatalities,
            "severity": a.severity_score(),
        }
        for a in accidents
    ]
    return render(request, 'map.html', {'accident_data': json.dumps(accident_data)})