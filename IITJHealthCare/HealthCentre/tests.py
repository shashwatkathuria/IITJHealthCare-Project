from django.test import Client, TestCase
from .models import Doctor, Patient, Prescription, passwordHasher, emailHasher

class DoctorsTestCase(TestCase):

    def setUp(self):

        email = "abcdefgh@gmail.com"
        passwordHash = passwordHasher("12345")
        emailHash = emailHasher(email)
        d1 = Doctor.objects.create(name = "Abcd Efgh", address = "Aaaa, Bbbbb, 110011", contactNumber = "8888888888", specialization = "ENT", email = email, passwordHash = passwordHash, emailHash = emailHash)

        email = "ijklmnop@gmail.com"
        passwordHash = passwordHasher("67890")
        emailHash = emailHasher(email)
        d2 = Doctor.objects.create(name = "Ijkl Mnop", address = "Cccc, Dddd, 001100", contactNumber = "9999999999", specialization = "EYE", email = email, passwordHash = passwordHash, emailHash = emailHash)

    def testDoctorCount(self):
        doctors = Doctor.objects.all()
        self.assertEqual(doctors.count(), 2)

    def testDoctorDetails(self):
        doctors = Doctor.objects.all()

        d1 = doctors[0]
        emailHash = emailHasher(d1.email)
        passwordHash = passwordHasher("12345")
        self.assertTrue(d1.name == "Abcd Efgh" and d1.address == "Aaaa, Bbbbb, 110011" and d1.contactNumber == "8888888888" and d1.specialization == "ENT" and d1.email == "abcdefgh@gmail.com" and d1.passwordHash == passwordHash and d1.emailHash == emailHash)

        d2 = doctors[1]
        emailHash = emailHasher(d2.email)
        passwordHash = passwordHasher("67890")
        self.assertTrue(d2.name == "Ijkl Mnop" and d2.address == "Cccc, Dddd, 001100" and d2.contactNumber == "9999999999" and d2.specialization == "EYE" and d2.email == "ijklmnop@gmail.com" and d2.passwordHash == passwordHash and d2.emailHash == emailHash)

    def testDuplicatePasswordHashes(self):
        doctors = Doctor.objects.all()
        passwordHashes = []
        for doctor in doctors:
            passwordHashes.append(doctor.passwordHash)

        passwordHashes = set(passwordHashes)
        passwordHashes = list(passwordHashes)

        self.assertEqual(len(passwordHashes), 2)

    def testDuplicateEmailHashes(self):
        doctors = Doctor.objects.all()
        emailHashes = []
        for doctor in doctors:
            emailHashes.append(doctor.emailHash)

        emailHashes = set(emailHashes)
        emailHashes = list(emailHashes)

        self.assertEqual(len(emailHashes), 2)

class PatientsTestCase(TestCase):

    def setUp(self):

        email = "12345@gmail.com"
        passwordHash = passwordHasher("abcdefgh")
        emailHash = emailHasher(email)
        p1 = Patient.objects.create(name = "Abcd Efgh", address = "Aaaa, Bbbbb, 110011", contactNumber = "8888888888", rollNumber = "B17CS101", email = email, passwordHash = passwordHash, emailHash = emailHash)

        email = "67890@gmail.com"
        passwordHash = passwordHasher("ijklmnop")
        emailHash = emailHasher(email)
        p2 = Patient.objects.create(name = "Ijkl Mnop", address = "Cccc, Dddd, 001100", contactNumber = "9999999999", rollNumber = "B17CS102", email = email, passwordHash = passwordHash, emailHash = emailHash)

    def testPatientCount(self):
        patients = Patient.objects.all()
        self.assertEqual(patients.count(), 2)

    def testpatientDetails(self):
        patients = Patient.objects.all()

        p1 = patients[0]
        emailHash = emailHasher(p1.email)
        passwordHash = passwordHasher("abcdefgh")
        self.assertTrue(p1.name == "Abcd Efgh" and p1.address == "Aaaa, Bbbbb, 110011" and p1.contactNumber == "8888888888" and p1.rollNumber == "B17CS101" and p1.email == "12345@gmail.com" and p1.passwordHash == passwordHash and p1.emailHash == emailHash)

        p2 = patients[1]
        emailHash = emailHasher(p2.email)
        passwordHash = passwordHasher("ijklmnop")
        self.assertTrue(p2.name == "Ijkl Mnop" and p2.address == "Cccc, Dddd, 001100" and p2.contactNumber == "9999999999" and p2.rollNumber == "B17CS102" and p2.email == "67890@gmail.com" and p2.passwordHash == passwordHash and p2.emailHash == emailHash)

    def testDuplicatePasswordHashes(self):
        patients = Patient.objects.all()
        passwordHashes = []
        for patient in patients:
            passwordHashes.append(patient.passwordHash)

        passwordHashes = set(passwordHashes)
        passwordHashes = list(passwordHashes)

        self.assertEqual(len(passwordHashes), 2)

    def testDuplicateEmailHashes(self):
        patients = Patient.objects.all()
        emailHashes = []
        for patient in patients:
            emailHashes.append(patient.emailHash)

        emailHashes = set(emailHashes)
        emailHashes = list(emailHashes)

        self.assertEqual(len(emailHashes), 2)

class PrescriptionsTestCase(TestCase):

    def setUp(self):

        email = "abcdefgh@gmail.com"
        passwordHash = passwordHasher("12345")
        emailHash = emailHasher(email)
        d1 = Doctor.objects.create(name = "Abcd Efgh", address = "Aaaa, Bbbbb, 110011", contactNumber = "8888888888", specialization = "ENT", email = email, passwordHash = passwordHash, emailHash = emailHash)

        email = "ijklmnop@gmail.com"
        passwordHash = passwordHasher("67890")
        emailHash = emailHasher(email)
        d2 = Doctor.objects.create(name = "Ijkl Mnop", address = "Cccc, Dddd, 001100", contactNumber = "9999999999", specialization = "EYE", email = email, passwordHash = passwordHash, emailHash = emailHash)

        email = "12345@gmail.com"
        passwordHash = passwordHasher("abcdefgh")
        emailHash = emailHasher(email)
        p1 = Patient.objects.create(name = "Abcd Efgh", address = "Aaaa, Bbbbb, 110011", contactNumber = "8888888888", rollNumber = "B17CS101", email = email, passwordHash = passwordHash, emailHash = emailHash)

        email = "67890@gmail.com"
        passwordHash = passwordHasher("ijklmnop")
        emailHash = emailHasher(email)
        p2 = Patient.objects.create(name = "Ijkl Mnop", address = "Cccc, Dddd, 001100", contactNumber = "9999999999", rollNumber = "B17CS102", email = email, passwordHash = passwordHash, emailHash = emailHash)

        symptoms = "aaaaa bbbbb"
        prescription1 = Prescription.objects.create(doctor = d1, patient = p1, symptoms = symptoms)

        symptoms = "ccccc ddddd"
        prescription2 = Prescription.objects.create(doctor = d2, patient = p2, symptoms = symptoms)

    def testPrescriptionCount(self):
        prescriptions = Prescription.objects.all()
        self.assertEqual(prescriptions.count(), 2)

    def testIncompletePrescription(self):
        prescriptions = Prescription.objects.all()
        for prescription in prescriptions:
            self.assertTrue(prescription.isNew)
            self.assertFalse(prescription.isCompleted)

    def testCompletePrescription(self):
        prescriptions = Prescription.objects.all()
        for prescription in prescriptions:
            prescription.prescriptionText = "Aaaaaa Bbbbbb Cccccc Dddddd"
            prescription.isNew = False
            prescription.isCompleted = True

        prescription1 = prescriptions[0]
        self.assertTrue(prescription1.doctor.id == Doctor.objects.get(email="abcdefgh@gmail.com").id and prescription1.patient.id == Patient.objects.get(email = "12345@gmail.com").id and prescription1.prescriptionText == "Aaaaaa Bbbbbb Cccccc Dddddd")
        self.assertTrue(prescription1.isCompleted)
        self.assertFalse(prescription1.isNew)

        prescription2 = prescriptions[1]
        self.assertTrue(prescription2.doctor.id == Doctor.objects.get(email="ijklmnop@gmail.com").id and prescription2.patient.id == Patient.objects.get(email = "67890@gmail.com").id and prescription2.prescriptionText == "Aaaaaa Bbbbbb Cccccc Dddddd")
        self.assertTrue(prescription2.isCompleted)
        self.assertFalse(prescription2.isNew)

def checkResponseHeaders(response):
    return response["Cache-Control"] == "no-cache, no-store, must-revalidate" and response["Pragma"] == "no-cache" and response["Expires"] == "0"

class ClientsInteractionTestCase(TestCase):

    def setUp(self):

        email = "abcdefgh@gmail.com"
        passwordHash = passwordHasher("12345")
        emailHash = emailHasher(email)
        d1 = Doctor.objects.create(name = "Abcd Efgh", address = "Aaaa, Bbbbb, 110011", contactNumber = "8888888888", specialization = "ENT", email = email, passwordHash = passwordHash, emailHash = emailHash)

        email = "ijklmnop@gmail.com"
        passwordHash = passwordHasher("67890")
        emailHash = emailHasher(email)
        d2 = Doctor.objects.create(name = "Ijkl Mnop", address = "Cccc, Dddd, 001100", contactNumber = "9999999999", specialization = "EYE", email = email, passwordHash = passwordHash, emailHash = emailHash)

        email = "12345@gmail.com"
        passwordHash = passwordHasher("abcdefgh")
        emailHash = emailHasher(email)
        p1 = Patient.objects.create(name = "Abcd Efgh", address = "Aaaa, Bbbbb, 110011", contactNumber = "8888888888", rollNumber = "B17CS101", email = email, passwordHash = passwordHash, emailHash = emailHash)

        email = "67890@gmail.com"
        passwordHash = passwordHasher("ijklmnop")
        emailHash = emailHasher(email)
        p2 = Patient.objects.create(name = "Ijkl Mnop", address = "Cccc, Dddd, 001100", contactNumber = "9999999999", rollNumber = "B17CS102", email = email, passwordHash = passwordHash, emailHash = emailHash)

        symptoms = "aaaaa bbbbb"
        prescription1 = Prescription.objects.create(doctor = d1, patient = p1, symptoms = symptoms)

        symptoms = "ccccc ddddd"
        prescription2 = Prescription.objects.create(doctor = d2, patient = p2, symptoms = symptoms)

    def testValidIndexPage(self):
        client = Client()

        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(checkResponseHeaders(response))

    def testValidContactUsPage(self):
        client = Client()

        response = client.get("/contactus")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(checkResponseHeaders(response))

    def testValidDoctorsPage(self):
        client = Client()

        response = client.get("/doctors")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(checkResponseHeaders(response))

        self.assertEqual(response.context["doctors"].count(), 2)

    def testGetEmergencyPage(self):
        client = Client()

        response = client.get("/emergency")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(checkResponseHeaders(response))

    def testPostEmergencyPage(self):
        client = Client()

        print("\n Testing...Emergency Message to be displayed on screen if everything works correctly.\n")
        response = client.post("/emergency", {'emergencyLocation':'XYZ Location'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(checkResponseHeaders(response))
        self.assertIn('XYZ Location', response.context['message'])

        response = client.post("/emergency", {'emergencyLocation':''})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(checkResponseHeaders(response))
        self.assertIn('Invalid input', response.context['message'])

    def testGetRegisterPage(self):
        client = Client()

        response = client.get("/register")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(checkResponseHeaders(response))

    def testPostRegisterPage(self):
        client = Client()

        response = client.post("/register", {"userFirstName" : "AA", "userLastName" : "BB", "userEmail" : "abcd@gmail.com", "userRollNo" : "B99CS099", "userAddress" : "CC, DD", "userContactNo" : "9999999999", "userPassword" : "12345", "userConfirmPassword" : "12345"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(checkResponseHeaders(response))
        self.assertIn("Registration Successful", response.context["message"])

        response = client.post("/register", {"userFirstName" : "AA", "userLastName" : "BB", "userEmail" : "abcd@gmail.com", "userRollNo" : "B99CS099", "userAddress" : "CC, DD", "userContactNo" : "9999999999", "userPassword" : "12345", "userConfirmPassword" : "123456"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(checkResponseHeaders(response))
        self.assertIn("Passwords do not match", response.context["message"])

    def testGetLoginPageWithNoSessionInfo(self):
        client = Client()

        response = client.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(checkResponseHeaders(response))

    def testPostDoctorLoginPage(self):
        client = Client()

        response = client.post("/login", {"useremail" : "notregisteredemail@gmail.com", "userpassword" : "123456"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(checkResponseHeaders(response))
        self.assertIn("User does not exist", response.context["message"])

        response = client.post("/login", {"useremail" : "abcdefgh@gmail.com", "userpassword" : "assumewrongpassword"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(checkResponseHeaders(response))
        self.assertIn("Invalid Credentials.", response.context["message"])

        response = client.post("/login", {"useremail" : "abcdefgh@gmail.com", "userpassword" : "12345"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(checkResponseHeaders(response))
        self.assertTrue(client.session["isLoggedIn"])
        self.assertTrue(client.session["isDoctor"])
        self.assertEqual(client.session["userEmail"], emailHasher("abcdefgh@gmail.com"))
        self.assertEqual(client.session["Name"], "Abcd Efgh")
        self.assertEqual(client.session["numberNewPrescriptions"], 1)

    def testGetDoctorLoginProfilePageWithSessionInfo(self):
        client = Client()

        client.post("/login", {"useremail" : "abcdefgh@gmail.com", "userpassword" : "12345"})
        response = client.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(checkResponseHeaders(response))
        self.assertTrue(client.session["isLoggedIn"])
        self.assertTrue(client.session["isDoctor"])
        self.assertEqual(client.session["userEmail"], emailHasher("abcdefgh@gmail.com"))
        self.assertEqual(client.session["Name"], "Abcd Efgh")
        self.assertEqual(client.session["numberNewPrescriptions"], 1)
        for prescription in response.context["user"]:
            self.assertEqual(prescription.doctor.email, "abcdefgh@gmail.com")
