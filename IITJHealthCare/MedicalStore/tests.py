from django.test import Client, TestCase
from django.urls import reverse
from .models import Medicine
import datetime

class MedicinesTestCase(TestCase):

    def setUp(self):

        m1 = Medicine.objects.create(name = "AA", company = "BB", manufacturedDate = datetime.datetime.now(), expiryDate = datetime.datetime.now() + datetime.timedelta(days = 365), quantity = 10, price = 100, photoId = "m00.jpg" )
        m2 = Medicine.objects.create(name = "CC", company = "DD", manufacturedDate = datetime.datetime.now(), expiryDate = datetime.datetime.now() + datetime.timedelta(days = 365 * 2), quantity = 50, price = 40, photoId = "m01.jpg" )
        m3 = Medicine.objects.create(name = "EE", company = "FF", manufacturedDate = datetime.datetime.now() + datetime.timedelta(days = 365 * 2), expiryDate = datetime.datetime.now() - datetime.timedelta(days = 365 * 2), quantity = 60, price = 70, photoId = "m02.jpg" )


    def testValidMedicineDate(self):
        medicines = Medicine.objects.all()

        for medicine in medicines:
            if medicine.name != "EE":
                self.assertTrue(medicine.expiryDate > medicine.manufacturedDate)
                self.assertTrue(medicine.expiryDate > datetime.datetime.now().date())

    def testInvalidMedicineDate(self):
        medicine = Medicine.objects.get(name = "EE")

        self.assertFalse(medicine.expiryDate > medicine.manufacturedDate)
        self.assertFalse(medicine.expiryDate > datetime.datetime.now().date())

    def testMedicineDetails(self):
        medicines = Medicine.objects.all()

        m1 = medicines[0]
        self.assertTrue(m1.name == "AA" and m1.company == "BB")

        m2 = medicines[1]
        self.assertTrue(m2.name == "CC" and m2.company == "DD")

        m3 = medicines[2]
        self.assertTrue(m3.name == "EE" and m3.company == "FF")

    def testMedicineQuantityAndPrice(self):
        medicines = Medicine.objects.all()

        for medicine in medicines:
            self.assertTrue(medicine.quantity >= 0)
            self.assertTrue(medicine.price > 0)

    def testMedicinePhotoId(self):
        medicines = Medicine.objects.all()

        validFormats = ['jpg', 'png', 'jpeg']

        for medicine in medicines:
            format = medicine.photoId.split(".")[1]
            self.assertTrue(format in validFormats)

class ClientWebInteraction(TestCase):

    def setUp(self):

        m1 = Medicine.objects.create(name = "AA", company = "BB", manufacturedDate = datetime.datetime.now(), expiryDate = datetime.datetime.now() + datetime.timedelta(days = 365), quantity = 10, price = 100, photoId = "m00.jpg" )
        m2 = Medicine.objects.create(name = "CC", company = "DD", manufacturedDate = datetime.datetime.now(), expiryDate = datetime.datetime.now() + datetime.timedelta(days = 365 * 2), quantity = 50, price = 40, photoId = "m01.jpg" )
        m3 = Medicine.objects.create(name = "EE", company = "FF", manufacturedDate = datetime.datetime.now() + datetime.timedelta(days = 365 * 2), expiryDate = datetime.datetime.now() - datetime.timedelta(days = 365 * 2), quantity = 60, price = 70, photoId = "m02.jpg" )

    def testIndexPage(self):
        client = Client()

        response = client.get(reverse('MedicalStore:index'))
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'MedicalStore/medicines.html', 'MedicalStore/layout.html')
