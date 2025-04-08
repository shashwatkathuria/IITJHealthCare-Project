from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Medicine
# Create your views here.


def index(request):
    """ Function for displaying main page of Medical Store. """

    # Getting all the medicines from the database
    medicines = Medicine.objects.all()

    # Storing all the medicines available inside context variable
    context = {
        "medicines" : medicines.order_by('name')
    }

    # Editing response headers so as to ignore cached versions of pages
    response = render(request, "MedicalStore/medicines.html", context)
    return responseHeadersModifier(response)

def search(request):
    """Function for displaying the search filtered medicines available in the database."""

    # If the user submits a search query
    if request.method == "POST":

        # Extracting the search query from post request
        searchQuery = request.POST["searchQuery"]

        # Getting the search results, i.e.,all the medicines containing
        # the search query as a substring
        searchFilteredMedicines = Medicine.objects.filter(name__contains = searchQuery)

        # Storing the search results inside the context variable
        context = {
            "medicines" : searchFilteredMedicines.order_by('name')
        }

        # Editing response headers so as to ignore cached versions of pages
        response = render(request, "MedicalStore/medicines.html", context)
        return responseHeadersModifier(response)

    # Redirecting if the request method is get as searching requires some input
    elif request.method == "GET":

        # Editing response headers so as to ignore cached versions of pages
        response = HttpResponseRedirect(reverse('MedicalStore:index'))
        return responseHeadersModifier(response)

    # Redirecting if the request method neither post nor get as searching requires some input
    else:

        # Editing response headers so as to ignore cached versions of pages
        response = HttpResponseRedirect(reverse('MedicalStore:index'))
        return responseHeadersModifier(response)

def responseHeadersModifier(response):
    """Funtion to edit response headers so that no cached versions can be viewed. Returns the modified response."""
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response
