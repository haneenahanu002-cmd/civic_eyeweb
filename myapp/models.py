from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Registration(models.Model):
    name=models.CharField(max_length=15)
    gender=models.CharField(max_length=10)
    photo=models.CharField(max_length=500)
    email=models.CharField(max_length=50)
    phone=models.CharField(max_length=20)
    place=models.CharField(max_length=20)
    city=models.CharField(max_length=30)
    state=models.CharField(max_length=30)
    pincode=models.CharField(max_length=10)
    USER=models.OneToOneField(User,on_delete=models.CASCADE)


class Department(models.Model):
    dname=models.CharField(max_length=200)
    description=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    USER=models.OneToOneField(User,on_delete=models.CASCADE)


class Complaint(models.Model):
    date=models.DateField()
    complaint=models.CharField(max_length=1000)
    photoproof=models.CharField(max_length=500)
    category=models.CharField(max_length=500)
    priority=models.CharField(max_length=500)
    solvedstatus=models.CharField(max_length=200)
    latitude=models.CharField(max_length=200)
    longitude=models.CharField(max_length=200)
    placename=models.CharField(max_length=100)
    REGISTRATION=models.ForeignKey(Registration,on_delete=models.CASCADE)
    DEPARTMENT=models.ForeignKey(Department,on_delete=models.CASCADE)

class Action(models.Model):
    date_of_action_taken=models.DateField()
    COMPLAINT=models.ForeignKey(Complaint, on_delete=models.CASCADE)
    action=models.CharField(max_length=1000,default='')

class Appreview(models.Model):
    review=models.CharField(max_length=500)
    rating=models.CharField(max_length=200)
    date=models.DateField()
    REGISTRATION=models.ForeignKey(Registration,on_delete=models.CASCADE)






