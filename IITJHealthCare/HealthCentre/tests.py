from django.test import Client, TestCase
from .models import Doctor, Patient, Prescription, passwordHasher

class DoctorsTestCase(TestCase):

    def setUp(self):

        passwordHash = passwordHasher("12345")
        d1 = Doctor.objects.create(name = "Abcd Efgh", address = "Aaaa, Bbbbb, 110011", contactNumber = "8888888888", email = "abcdefgh@gmail.com", password = passwordHash)

        passwordHash = passwordHasher("67890")
        d2 = Doctor.objects.create(name = "Ijkl Mnop", address = "Cccc, Dddd, 001100", contactNumber = "9999999999", email = "ijklmnop@gmail.com", password = passwordHash)

    def testDoctorCount(self):
        doctors = Doctor.objects.all()
        self.assertEqual(doctors.count(), 2)

    def testDuplicatePasswordHashes(self):
        doctors = Doctor.objects.all()
        passwordHashes = []
        for doctor in doctors:
            passwordHashes.append(doctor.password)

        passwordHashes = set(passwordHashes)
        passwordHashes = list(passwordHashes)

        self.assertEqual(len(passwordHashes), 2)
