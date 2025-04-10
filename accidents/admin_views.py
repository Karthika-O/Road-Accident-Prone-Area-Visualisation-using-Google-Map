import random
import string

from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
import datetime

from accidents.models import Authority, UserType

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/index.html'
    login_url = '/'

class NewAuthority(TemplateView):
    template_name = 'admin/new_Authority.html'
    
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
                return render(request, 'admin/index.html', {'message': messages})
            except:
                messages = "Enter Another Username"
                return render(request, 'admin/index.html', {'message': messages})
        else:
            messages = "Age is not Eligible"
            return render(request, 'admin/index.html', {'message': messages})



class View_Authority(TemplateView):
    template_name = 'admin/view_Authority.html'
    def get_context_data(self, **kwargs):
        context = super(View_Authority, self).get_context_data(**kwargs)
        com = Authority.objects.all()
        context['com'] = com
        return context
    
class ApproveView(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        user = User.objects.get(pk=id)
        user.last_name = '1'

        user.save()
        return render(request, 'admin/index.html', {'message': "Account Activated"})


class RejectView(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        user = User.objects.get(pk=id)
        user.last_name = '0'
        user.is_active = '0'
        user.save()
        return render(request, 'admin/index.html', {'message': "Account Removed"})