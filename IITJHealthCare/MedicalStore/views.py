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
    return responseHeadersModifier(response)

def search(request):
    if request.method == "POST":
        searchQuery = request.POST["searchQuery"]

        searchFilteredMedicines = Medicine.objects.filter(name__contains = searchQuery)

        context = {
            "medicines" : searchFilteredMedicines.order_by('name')
        }

        response = render(request, "MedicalStore/medicines.html", context)
        return responseHeadersModifier(response)

    elif request.method == "GET":
        response = HttpResponseRedirect(reverse('MedicalStore:index'))
        return responseHeadersModifier(response)

    else:
        response = HttpResponseRedirect(reverse('MedicalStore:index'))
        return responseHeadersModifier(response)

def responseHeadersModifier(response):
    """Funtion to edit response headers so that no cached versions can be viewed. Returns the modified response."""
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response
