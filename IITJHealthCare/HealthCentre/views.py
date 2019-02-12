from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Doctor, Patient, Prescription
from Crypto.Hash import SHA256
from codecs import encode,decode

# Create your views here.

def index(request):
    # if request.user.is_authenticated
    return render(request,"HealthCentre/index.html")

def register(request):
    if request.method == "GET":
        return render(request,"HealthCentre/register.html")

    elif request.method == "POST":
        userFirstName = request.POST["userFirstName"]
        userLastName = request.POST["userLastName"]
        userEmail = request.POST["userEmail"]
        userRollNo = request.POST["userRollNo"]
        userAddress = request.POST["userAddress"]
        userContactNo = request.POST["userContactNo"]
        userPassword = request.POST["userPassword"]
        userConfirmPassword = request.POST["userConfirmPassword"]
        if userPassword == userConfirmPassword:
            name = userFirstName + " " + userLastName
            SHA256Engine = SHA256.new()
            userPassword = userPassword.encode()
            SHA256Engine.update(userPassword)
            passwordHash = SHA256Engine.digest()
            passwordHash = encode(passwordHash, 'hex')
            passwordHash = decode(passwordHash, 'utf-8')
            patient = Patient(name = name,rollNumber = userRollNo, email = userEmail, password = passwordHash, address = userAddress, contactNumber = userContactNo )
            patient.save()
            context = {
                "message":"User Registration Successful. Please Login."
            }
            return render(request, "HealthCentre/register.html",context)

        else:
            context = {
                "message":"Passwords do not match.Please register again."
            }
            return render(request,"HealthCentre/register.html",context)
    else:
        return render(request,"HealthCentre/register.html")

def doctors(request):

    context = {
        "doctors" : Doctor.objects.all()
    }
    return render(request,"HealthCentre/doctors.html",context)

def login(request):
    if request.method == "GET":
        return render(request,"HealthCentre/login.html")
    elif request.method == "POST":
        # username = request.POST["useremail"]
        # password = request.POST["userpassword"]
        # patient = Patient.objects.get(email = useremail)

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,"HealthCentre/login.html")

def emergency(request):
    return render(request,"HealthCentre/emergency.html")
