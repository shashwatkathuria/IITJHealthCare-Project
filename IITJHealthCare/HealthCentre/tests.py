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
