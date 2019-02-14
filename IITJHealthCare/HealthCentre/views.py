from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Doctor, Patient, Prescription
from Crypto.Hash import SHA256
from codecs import encode,decode
from django.db.models import Count, Q

# Create your views here.

def index(request):

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
        try:
            if request.session['isLoggedIn']:

                patient = Patient.objects.get(email = request.session['userEmail'])

                records = patient.patientRecords.all()
                numberNewPrescriptions = patient.patientRecords.aggregate(newPrescriptions = Count('pk', filter = Q(isNew = True)))['newPrescriptions']
                request.session['numberNewPrescriptions'] = numberNewPrescriptions
                for record in records:
                    record.new = False
                    record.save()

                context = {
                    "message" : "Successfully Logged In.",
                    "isAuthenticated" : True,
                    "user": records.order_by('-timestamp')
                    }

                return render(request,"HealthCentre/userPatientInfo.html", context)
            else:
                return render(request,"HealthCentre/login.html")
        except:
            return render(request,"HealthCentre/login.html")

    elif request.method == "POST":

        userName = request.POST["useremail"]
        userPassword = request.POST["userpassword"]

        try:
            patient = Patient.objects.get(email = userName)

        except Patient.DoesNotExist:
            context = {
                "message":"User does not exist.Please register first."
            }
            return render(request,"HealthCentre/login.html", context)

        SHA256Engine = SHA256.new()
        userPassword = userPassword.encode()
        SHA256Engine.update(userPassword)
        passwordHash = SHA256Engine.digest()
        passwordHash = encode(passwordHash, 'hex')
        passwordHash = decode(passwordHash, 'utf-8')

        records = patient.patientRecords.all()
        numberNewPrescriptions = patient.patientRecords.aggregate(newPrescriptions = Count('pk', filter = Q(isNew = True)))['newPrescriptions']
        request.session['numberNewPrescriptions'] = numberNewPrescriptions
        for record in records:
            record.new = False
            record.save()

        if passwordHash == patient.password:

            context = {
                "message" : "Successfully Logged In.",
                "isAuthenticated" : True,
                "user": records.order_by('-timestamp')
            }
            request.session['isLoggedIn'] = True
            request.session['userEmail'] = userName
            request.session['Name'] = patient.name

            return render(request,"HealthCentre/userPatientInfo.html", context)

        else:

            context = {
                "message":"Invalid Credentials.Please Try Again."
            }

            return render(request,"HealthCentre/login.html", context)

    else:
        return render(request,"HealthCentre/login.html")

def emergency(request):

    if request.method == "GET":
        return render(request,"HealthCentre/emergency.html")

    elif request.method == "POST":

        emergencyLocation = request.POST['emergencyLocation']

        if emergencyLocation != "":
            print("------------------------------------------------------------------------")
            print("\n\nEMERGENCY !! AMBULANCE REQUIRED AT " + emergencyLocation + " !!\n\n")
            print("------------------------------------------------------------------------")

            context = {
                "message" : "Ambulance reaching " + emergencyLocation + " in 2 minutes."
            }

            return render(request, "HealthCentre/emergency.html", context)

        else:
            errorMessage = "No location entered.Invalid input."

            context = {
                "message" : errorMessage
            }

            return render(request, "HealthCentre/emergency.html", context)

    else:
        return render(request,"HealthCentre/emergency.html")

def logout(request):

    request.session['isLoggedIn'] = False
    request.session['userEmail'] = ""
    request.session['Name'] = ""
    request.session['numberNewPrescriptions'] = 0

    context = {
        "message":"Successfully Logged Out."
    }

    return HttpResponseRedirect(reverse('login'))

def contactus(request):
    return render(request, "HealthCentre/contactus.html")
