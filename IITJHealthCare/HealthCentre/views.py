from django.http import HttpResponse
from django.shortcuts import render
from .models import Doctor, Patient, Prescription

# Create your views here.

def index(request):

    # return HttpResponse("Welcome to the Health Centre!")
    return render(request,"HealthCentre/index.html")

def register(request):

    # return HttpResponse("Welcome to the Health Centre!")
    return render(request,"HealthCentre/register.html")

def doctors(request):

    context = {
        "doctors" : Doctor.objects.all()
    }
    return render(request,"HealthCentre/doctors.html",context)
