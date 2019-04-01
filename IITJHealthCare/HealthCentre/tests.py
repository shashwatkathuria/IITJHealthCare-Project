from django.test import Client, TestCase
from .models import Doctor, Patient, Prescription, passwordHasher, emailHasher

class DoctorsTestCase(TestCase):

    def setUp(self):

        email = "abcdefgh@gmail.com"
        passwordHash = passwordHasher("12345")
        emailHash = emailHasher(email)
        d1 = Doctor.objects.create(name = "Abcd Efgh", address = "Aaaa, Bbbbb, 110011", contactNumber = "8888888888", email = email, passwordHash = passwordHash, emailHash = emailHash)

        email = "ijklmnop@gmail.com"
        passwordHash = passwordHasher("67890")
        emailHash = emailHasher(email)
        d2 = Doctor.objects.create(name = "Ijkl Mnop", address = "Cccc, Dddd, 001100", contactNumber = "9999999999", email = email, passwordHash = passwordHash, emailHash = emailHash)

    def testDoctorCount(self):
        doctors = Doctor.objects.all()
        self.assertEqual(doctors.count(), 2)

    def testDuplicatePasswordHashes(self):
        doctors = Doctor.objects.all()
        passwordHashes = []
        for doctor in doctors:
            passwordHashes.append(doctor.passwordHash)

        passwordHashes = set(passwordHashes)
        passwordHashes = list(passwordHashes)

        self.assertEqual(len(passwordHashes), 2)
