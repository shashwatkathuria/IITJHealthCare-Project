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

        return render(request,"HealthCentre/registrationPortal.html")

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

            return render(request, "HealthCentre/registrationPortal.html",context)

        else:
            context = {
                "message":"Passwords do not match.Please register again."
            }

            return render(request,"HealthCentre/registrationPortal.html",context)
    else:
        return render(request,"HealthCentre/registrationPortal.html")


def doctors(request):

    context = {
        "doctors" : Doctor.objects.all()
    }
    return render(request,"HealthCentre/doctors.html",context)


def login(request):
    if request.method == "GET":
        try:
            if request.session['isLoggedIn'] and request.session['isDoctor']:
                doctor = Doctor.objects.get(email = request.session['userEmail'])
                records = doctor.doctorRecords.all()
                numberNewPendingPrescriptions = doctor.doctorRecords.aggregate(newPendingPrescriptions = Count('pk', filter =( Q(isNew = True) & Q(isCompleted = False) ) ))['newPendingPrescriptions']
                request.session['numberNewPrescriptions'] = numberNewPendingPrescriptions


                context = {
                    "message" : "Successfully Logged In.",
                    "isAuthenticated" : True,
                    "user": records.order_by('-timestamp')
                }

                return render(request,"HealthCentre/userDoctorProfilePortal.html", context)

            elif request.session['isLoggedIn'] and (not request.session['isDoctor']):

                patient = Patient.objects.get(email = request.session['userEmail'])

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

                return render(request,"HealthCentre/userPatientProfilePortal.html", context)
            else:
                return render(request,"HealthCentre/loginPortal.html")
        except:
            return render(request,"HealthCentre/loginPortal.html")

    elif request.method == "POST":

        userName = request.POST["useremail"]
        userPassword = request.POST["userpassword"]


        try:
            patient = Patient.objects.get(email = userName)

        except Patient.DoesNotExist:
            try:
                doctor = Doctor.objects.get(email = userName)
                request.session['isDoctor'] = True
            except Doctor.DoesNotExist:
                context = {
                    "message":"User does not exist.Please register first."
                }
                return render(request,"HealthCentre/loginPortal.html", context)

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
                request.session['userEmail'] = userName
                request.session['Name'] = doctor.name

                return render(request,"HealthCentre/userDoctorProfilePortal.html", context)

            else:
                context = {
                    "message":"Invalid Credentials.Please Try Again."
                }

                return render(request,"HealthCentre/loginPortal.html", context)

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
                request.session['userEmail'] = userName
                request.session['Name'] = patient.name
                request.session['isDoctor'] = False

                return render(request,"HealthCentre/userPatientProfilePortal.html", context)

            else:

                context = {
                    "message":"Invalid Credentials.Please Try Again."
                }

                return render(request,"HealthCentre/loginPortal.html", context)

    else:
        return render(request,"HealthCentre/loginPortal.html")

def emergency(request):

    if request.method == "GET":
        return render(request,"HealthCentre/emergencyPortal.html")

    elif request.method == "POST":

        emergencyLocation = request.POST['emergencyLocation']

        if emergencyLocation != "":
            print("------------------------------------------------------------------------")
            print("\n\nEMERGENCY !! AMBULANCE REQUIRED AT " + emergencyLocation + " !!\n\n")
            print("------------------------------------------------------------------------")

            context = {
                "message" : "Ambulance reaching " + emergencyLocation + " in 2 minutes."
            }

            return render(request, "HealthCentre/emergencyPortal.html", context)

        else:
            errorMessage = "No location entered.Invalid input."

            context = {
                "message" : errorMessage
            }

            return render(request, "HealthCentre/emergencyPortal.html", context)

    else:
        return render(request,"HealthCentre/emergencyPortal.html")

def logout(request):

    request.session['isDoctor'] = False
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

def onlineprescription(request):
    if request.method == "GET":
        if request.session['isLoggedIn']:
            if request.session['isDoctor']:
                context = {
                        "message":"Only for patients."
                }
                print("Hello")
                return render(request, "HealthCentre/prescriptionPortal.html", context)
            else:
                context = {
                    "doctors" : Doctor.objects.all().order_by('specialization')
                }
                return render(request, "HealthCentre/prescriptionPortal.html", context)
        else:
            context = {
                    "message":"Please Login First."
            }
            return render(request, "HealthCentre/prescriptionPortal.html", context)

    elif request.method == "POST":
        if request.session['isLoggedIn']:
            if request.session['isDoctor']:
                prescriptionText = request.POST['prescription']
                prescription = Prescription.objects.get(pk = request.POST['prescriptionID'])
                prescription.prescriptionText = prescriptionText
                prescription.isCompleted = True
                prescription.isNew = True
                prescription.save()
                records = Doctor.objects.get(email = request.session['userEmail']).doctorRecords.all()
                context = {
                    "user" : records,
                    "successPrescriptionMessage" : "Prescription Successfully Submitted."
                }

                return render(request, "HealthCentre/userDoctorProfilePortal.html", context)


            else:
                doctor = Doctor.objects.get(pk = request.POST["doctor"])
                symptoms = request.POST["symptoms"]
                prescription = Prescription(doctor = doctor, patient = Patient.objects.get(email = request.session['userEmail']), symptoms = symptoms)
                prescription.save()
                context = {
                    "successPrescriptionMessage" : "Prescription Successfully Requested.",
                    "doctors"  : Doctor.objects.all().order_by('specialization')
                }
                return render(request, "HealthCentre/prescriptionPortal.html", context)
        else:
            context = {
                    "successPrescriptionMessage":"Please Login First.",
            }
            return render(request, "HealthCentre/loginPortal.html", context)

    else:
        return render(request, "HealthCentre/prescriptionPortal.html")
