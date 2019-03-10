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

    response = render(request,"HealthCentre/index.html")
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response


def register(request):

    if request.method == "GET":

        response =  render(request,"HealthCentre/registrationPortal.html")
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"
        return response

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

            SHA256Engine = SHA256.new()
            userEmail = userEmail.encode()
            SHA256Engine.update(userEmail)
            emailHash = SHA256Engine.digest()
            emailHash = encode(emailHash, 'hex')
            emailHash = decode(emailHash, 'utf-8')

            patient = Patient(name = name,rollNumber = userRollNo, email = userEmail, password = passwordHash, address = userAddress, contactNumber = userContactNo, emailHash = emailHash )
            patient.save()

            context = {
                "message":"User Registration Successful. Please Login."
            }

            response = render(request, "HealthCentre/registrationPortal.html",context)
            response["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"
            return response

        else:
            context = {
                "message":"Passwords do not match.Please register again."
            }

            response = render(request,"HealthCentre/registrationPortal.html",context)
            response["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"
            return response
    else:
        response = render(request,"HealthCentre/registrationPortal.html")
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"
        return response


def doctors(request):

    context = {
        "doctors" : Doctor.objects.all()
    }
    response = render(request,"HealthCentre/doctors.html",context)
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response


def login(request):
    if request.method == "GET":
        try:
            if request.session['isLoggedIn'] and request.session['isDoctor']:
                doctor = Doctor.objects.get(emailHash = request.session['userEmail'])
                records = doctor.doctorRecords.all()
                numberNewPendingPrescriptions = doctor.doctorRecords.aggregate(newPendingPrescriptions = Count('pk', filter =( Q(isNew = True) & Q(isCompleted = False) ) ))['newPendingPrescriptions']
                request.session['numberNewPrescriptions'] = numberNewPendingPrescriptions


                context = {
                    "message" : "Successfully Logged In.",
                    "isAuthenticated" : True,
                    "user": records.order_by('-timestamp')
                }

                response = render(request,"HealthCentre/userDoctorProfilePortal.html", context)
                response["Cache-Control"] = "no-cache, no-store, must-revalidate"
                response["Pragma"] = "no-cache"
                response["Expires"] = "0"
                return response

            elif request.session['isLoggedIn'] and (not request.session['isDoctor']):

                patient = Patient.objects.get(emailHash = request.session['userEmail'])

                records = patient.patientRecords.all()
                numberNewPrescriptions = patient.patientRecords.aggregate(newCompletedPrescriptions = Count('pk', filter =( Q(isNew = True) & Q(isCompleted = True) ) ) )['newCompletedPrescriptions']
                request.session['numberNewPrescriptions'] = numberNewPrescriptions
                for record in records:
                    if record.isCompleted  :
                        record.isNew = False
                        record.save()

                context = {
                    "message" : "Successfully Logged In.",
                    "isAuthenticated" : True,
                    "user": records.order_by('-timestamp')
                    }

                response = render(request,"HealthCentre/userPatientProfilePortal.html", context)
                response["Cache-Control"] = "no-cache, no-store, must-revalidate"
                response["Pragma"] = "no-cache"
                response["Expires"] = "0"
                return response
            else:
                response = render(request,"HealthCentre/loginPortal.html")
                response["Cache-Control"] = "no-cache, no-store, must-revalidate"
                response["Pragma"] = "no-cache"
                response["Expires"] = "0"
                return response
        except:
            response = render(request,"HealthCentre/loginPortal.html")
            response["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"
            return response

    elif request.method == "POST":
        userName = request.POST["useremail"]
        userPassword = request.POST["userpassword"]


        try:
            patient = Patient.objects.get(email = userName)
            request.session['isDoctor'] = False

        except Patient.DoesNotExist:
            try:
                doctor = Doctor.objects.get(email = userName)
                request.session['isDoctor'] = True
            except Doctor.DoesNotExist:
                context = {
                    "message":"User does not exist.Please register first."
                }
                response = render(request,"HealthCentre/loginPortal.html", context)
                response["Cache-Control"] = "no-cache, no-store, must-revalidate"
                response["Pragma"] = "no-cache"
                response["Expires"] = "0"
                return response

        SHA256Engine = SHA256.new()
        userPassword = userPassword.encode()
        SHA256Engine.update(userPassword)
        passwordHash = SHA256Engine.digest()
        passwordHash = encode(passwordHash, 'hex')
        passwordHash = decode(passwordHash, 'utf-8')

        if request.session['isDoctor']:
            records = doctor.doctorRecords.all()
            numberNewPendingPrescriptions = doctor.doctorRecords.aggregate(newPendingPrescriptions = Count('pk', filter =( Q(isNew = True) & Q(isCompleted = False) ) ))['newPendingPrescriptions']
            request.session['numberNewPrescriptions'] = numberNewPendingPrescriptions

            if passwordHash == doctor.password:

                context = {
                    "message" : "Successfully Logged In.",
                    "isAuthenticated" : True,
                    "user": records.order_by('-timestamp')
                }
                request.session['isLoggedIn'] = True
                request.session['userEmail'] = doctor.emailHash
                request.session['Name'] = doctor.name

                response = HttpResponseRedirect(reverse('index'))
                response["Cache-Control"] = "no-cache, no-store, must-revalidate"
                response["Pragma"] = "no-cache"
                response["Expires"] = "0"
                return response

            else:
                context = {
                    "message":"Invalid Credentials.Please Try Again."
                }

                response = render(request,"HealthCentre/loginPortal.html", context)
                response["Cache-Control"] = "no-cache, no-store, must-revalidate"
                response["Pragma"] = "no-cache"
                response["Expires"] = "0"
                return response

        else:
            records = patient.patientRecords.all()
            numberNewPrescriptions = patient.patientRecords.aggregate(newCompletedPrescriptions = Count('pk', filter =( Q(isNew = True) & Q(isCompleted = True) ) ))['newCompletedPrescriptions']
            request.session['numberNewPrescriptions'] = numberNewPrescriptions
            for record in records:
                if record.isCompleted  :
                    record.isNew = False
                    record.save()

            if passwordHash == patient.password:

                context = {
                    "message" : "Successfully Logged In.",
                    "isAuthenticated" : True,
                    "user": records.order_by('-timestamp')
                }
                request.session['isLoggedIn'] = True
                request.session['userEmail'] = patient.emailHash
                request.session['Name'] = patient.name
                request.session['isDoctor'] = False

                response = HttpResponseRedirect(reverse('index'))
                response["Cache-Control"] = "no-cache, no-store, must-revalidate"
                response["Pragma"] = "no-cache"
                response["Expires"] = "0"
                return response

            else:

                context = {
                    "message":"Invalid Credentials.Please Try Again."
                }

                response = render(request,"HealthCentre/loginPortal.html", context)
                response["Cache-Control"] = "no-cache, no-store, must-revalidate"
                response["Pragma"] = "no-cache"
                response["Expires"] = "0"
                return response

    else:
        response = render(request,"HealthCentre/loginPortal.html")
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"
        return response

def emergency(request):

    if request.method == "GET":
        response = render(request,"HealthCentre/emergencyPortal.html")
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"
        return response

    elif request.method == "POST":

        emergencyLocation = request.POST['emergencyLocation']

        if emergencyLocation != "":
            print("------------------------------------------------------------------------")
            print("\n\nEMERGENCY !! AMBULANCE REQUIRED AT " + emergencyLocation + " !!\n\n")
            print("------------------------------------------------------------------------")

            context = {
                "message" : "Ambulance reaching " + emergencyLocation + " in 2 minutes."
            }

            response = render(request, "HealthCentre/emergencyPortal.html", context)
            response["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"
            return response

        else:
            errorMessage = "No location entered.Invalid input."

            context = {
                "message" : errorMessage
            }

            response = render(request, "HealthCentre/emergencyPortal.html", context)
            response["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"
            return response

    else:
        response = render(request,"HealthCentre/emergencyPortal.html")
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"
        return response

def logout(request):

    request.session['isDoctor'] = False
    request.session['isLoggedIn'] = False
    request.session['userEmail'] = ""
    request.session['Name'] = ""
    request.session['numberNewPrescriptions'] = 0

    context = {
        "message":"Successfully Logged Out."
    }

    response = HttpResponseRedirect(reverse('login'))
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response

def contactus(request):
    response = render(request, "HealthCentre/contactus.html")
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response

def onlineprescription(request):
    if request.method == "GET":
        if request.session['isLoggedIn']:
            if request.session['isDoctor']:
                context = {
                        "message":"Only for patients."
                }
                print("Hello")
                response = render(request, "HealthCentre/prescriptionPortal.html", context)
                response["Cache-Control"] = "no-cache, no-store, must-revalidate"
                response["Pragma"] = "no-cache"
                response["Expires"] = "0"
                return response
            else:
                context = {
                    "doctors" : Doctor.objects.all().order_by('specialization')
                }
                response = render(request, "HealthCentre/prescriptionPortal.html", context)
                response["Cache-Control"] = "no-cache, no-store, must-revalidate"
                response["Pragma"] = "no-cache"
                response["Expires"] = "0"
                return response
        else:
            context = {
                    "message":"Please Login First."
            }
            response = render(request, "HealthCentre/prescriptionPortal.html", context)
            response["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"
            return response

    elif request.method == "POST":
        if request.session['isLoggedIn']:
            if request.session['isDoctor']:
                prescriptionText = request.POST['prescription']
                prescription = Prescription.objects.get(pk = request.POST['prescriptionID'])
                prescription.prescriptionText = prescriptionText
                prescription.isCompleted = True
                prescription.isNew = True
                prescription.save()
                records = Doctor.objects.get(emailHash = request.session['userEmail']).doctorRecords.all()
                context = {
                    "user" : records,
                    "successPrescriptionMessage" : "Prescription Successfully Submitted."
                }

                response = render(request, "HealthCentre/userDoctorProfilePortal.html", context)
                response["Cache-Control"] = "no-cache, no-store, must-revalidate"
                response["Pragma"] = "no-cache"
                response["Expires"] = "0"
                return response


            else:
                doctor = Doctor.objects.get(pk = request.POST["doctor"])
                symptoms = request.POST["symptoms"]
                prescription = Prescription(doctor = doctor, patient = Patient.objects.get(emailHash = request.session['userEmail']), symptoms = symptoms)
                prescription.save()
                context = {
                    "successPrescriptionMessage" : "Prescription Successfully Requested.",
                    "doctors"  : Doctor.objects.all().order_by('specialization')
                }
                response = render(request, "HealthCentre/prescriptionPortal.html", context)
                response["Cache-Control"] = "no-cache, no-store, must-revalidate"
                response["Pragma"] = "no-cache"
                response["Expires"] = "0"
                return response
        else:
            context = {
                    "successPrescriptionMessage":"Please Login First.",
            }
            response = render(request, "HealthCentre/loginPortal.html", context)
            response["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"
            return response

    else:
        response = render(request, "HealthCentre/prescriptionPortal.html")
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"
        return response
