from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Medicine
# Create your views here.


def index(request):
    medicines = Medicine.objects.all()
    
    context = {
        "medicines" : medicines.order_by('name')
    }

    response = render(request, "MedicalStore/medicines.html", context)
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response
