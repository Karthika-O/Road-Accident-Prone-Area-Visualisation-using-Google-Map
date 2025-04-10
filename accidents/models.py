from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserType(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)

class Authority(models.Model):
    pfirstna=models.CharField(max_length=200, null=True, blank=True)
    plastna = models.CharField(max_length=200, null=True, blank=True)
    pbadgeno=models.IntegerField(null=True)
    pdesign=models.CharField(max_length=200,null=True,blank=True)
    pjuri=models.CharField(max_length=200,null=True,blank=True)
    pcontact = models.CharField(max_length=200, null=True, blank=True)
    pdob = models.CharField(max_length=200, null=True, blank=True)
    pgender = models.CharField(max_length=200, null=True, blank=True)
    pPermanantAddress = models.CharField(max_length=200, null=True, blank=True)
    pTemporaryAddress = models.CharField(max_length=200, null=True, blank=True)
    pDistrict = models.CharField(max_length=200, null=True, blank=True)
    pIDproof = models.ImageField(
        max_length=200, upload_to='image/', null=True, blank=True)
    pPhoto = models.ImageField(
        max_length=200, upload_to='image/', null=True, blank=True)
    email=models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
   
class Accident(models.Model):
    district = models.CharField(max_length=100)
    police_station = models.CharField(max_length=100)
    location = models.TextField()
    road_name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    total_accidents = models.IntegerField(default=0)
    total_fatalities = models.IntegerField(default=0)
    def severity_score(self):
        return (self.total_accidents * 0.7) + (self.total_fatalities * 1.5)
    def __str__(self):
        return f"{self.location} - {self.road_name}"
 