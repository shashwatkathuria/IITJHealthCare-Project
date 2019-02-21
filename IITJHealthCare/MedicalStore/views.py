from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Medicine
# Create your views here.


def index(request):
    medicines = Medicine.objects.all()
    context = {
        "medicines" : medicines
    }
    return render(request, "MedicalStore/medicines.html", context)
