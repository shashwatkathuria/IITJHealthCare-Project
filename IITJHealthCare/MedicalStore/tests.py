from django.test import Client, TestCase
from django.urls import reverse
from .models import Medicine
import datetime

class MedicinesTestCase(TestCase):

    def setUp(self):
        """Function to create and save medicines required for testing in the database."""

        # Creating and saving medicines required for testing

        # Medicines with correct entries
        m1 = Medicine.objects.create(name = "AA", company = "BB", manufacturedDate = datetime.datetime.now(), expiryDate = datetime.datetime.now() + datetime.timedelta(days = 365), quantity = 10, price = 100, photoId = "m00.jpg" )
        m2 = Medicine.objects.create(name = "CC", company = "DD", manufacturedDate = datetime.datetime.now(), expiryDate = datetime.datetime.now() + datetime.timedelta(days = 365 * 2), quantity = 50, price = 40, photoId = "m01.jpg" )

        # Medicine with incorrect entries, manufactured date is after expiry date
        m3 = Medicine.objects.create(name = "EE", company = "FF", manufacturedDate = datetime.datetime.now() + datetime.timedelta(days = 365 * 2), expiryDate = datetime.datetime.now() - datetime.timedelta(days = 365 * 2), quantity = 60, price = 70, photoId = "m02.jpg" )


    def testValidMedicineDate(self):
        """Funtion to test the manufactured and expiry dates of valid(correct) medicines."""

        # Getting all the medicines from the database
        medicines = Medicine.objects.all()

        # Checking for each medicine except the incorrect one
        for medicine in medicines:
            if medicine.name != "EE":
                # Asserting correct order of dates, i.e, expiry should be after manufacturing
                # as well as after the current date
                self.assertTrue(medicine.expiryDate > medicine.manufacturedDate)
                self.assertTrue(medicine.expiryDate > datetime.datetime.now().date())

    def testInvalidMedicineDate(self):
        """Funtion to test the manufactured and expiry dates of invalid(wrong) medicines."""

        # Getting the incorrect medicine from the database
        medicine = Medicine.objects.get(name = "EE")

        # Asserting the false attributes, i.e., the incorrect expiry and manufactured dates
        self.assertFalse(medicine.expiryDate > medicine.manufacturedDate)
        self.assertFalse(medicine.expiryDate > datetime.datetime.now().date())

    def testMedicineDetails(self):
        """Function to test the details except dates for each of the medicines."""

        # Getting all the medicines from the database
        medicines = Medicine.objects.all()

        # Asserting for each medicine, its correct name and company

        m1 = medicines[0]
        self.assertTrue(m1.name == "AA" and m1.company == "BB")

        m2 = medicines[1]
        self.assertTrue(m2.name == "CC" and m2.company == "DD")

        m3 = medicines[2]
        self.assertTrue(m3.name == "EE" and m3.company == "FF")

    def testMedicineQuantityAndPrice(self):
        """Function to confirm that all the medicines have nonnegative quantities and positive prices."""

        # Getting all the medicines from the database
        medicines = Medicine.objects.all()

        # For each medicine, checking its price and quantity
        for medicine in medicines:
            # Asserting that the quantity is nonnegative and the price is positive
            self.assertTrue(medicine.quantity >= 0)
            self.assertTrue(medicine.price > 0)

    def testMedicinePhotoId(self):
        """Function to confirm the correct image formats for the medicine images."""

        # Getting all the medicines from the database
        medicines = Medicine.objects.all()

        # Initializing a list of valid image formats accepted
        validFormats = ['jpg', 'png', 'jpeg']

        # For each medicine, checking the format of its photo
        for medicine in medicines:
            # Extracting format of medicine
            format = medicine.photoId.split(".")[1]
            # Asserting that the format is in the valid formats
            self.assertTrue(format in validFormats)

def checkResponseHeaders(response):
    return response["Cache-Control"] == "no-cache, no-store, must-revalidate" and response["Pragma"] == "no-cache" and response["Expires"] == "0"

class ClientWebInteraction(TestCase):

    def setUp(self):

        m1 = Medicine.objects.create(name = "abcdef", company = "BB", manufacturedDate = datetime.datetime.now(), expiryDate = datetime.datetime.now() + datetime.timedelta(days = 365), quantity = 10, price = 100, photoId = "m00.jpg" )
        m2 = Medicine.objects.create(name = "defghi", company = "DD", manufacturedDate = datetime.datetime.now(), expiryDate = datetime.datetime.now() + datetime.timedelta(days = 365 * 2), quantity = 50, price = 40, photoId = "m01.jpg" )
        m3 = Medicine.objects.create(name = "wxyzpqrs", company = "FF", manufacturedDate = datetime.datetime.now() + datetime.timedelta(days = 365 * 2), expiryDate = datetime.datetime.now() - datetime.timedelta(days = 365 * 2), quantity = 60, price = 70, photoId = "m02.jpg" )

    def testIndexPage(self):
        client = Client()

        response = client.get(reverse('MedicalStore:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(checkResponseHeaders(response))
        self.assertTemplateUsed(response, 'MedicalStore/medicines.html', 'MedicalStore/layout.html')

    def testPostSearchPage(self):
        client = Client()

        response = client.post(reverse('MedicalStore:search'), {'searchQuery' : 'ef'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(checkResponseHeaders(response))
        self.assertTemplateUsed(response, 'MedicalStore/medicines.html', 'MedicalStore/layout.html')
        for medicine in response.context['medicines']:
            self.assertIn('ef', medicine.name)

    def testGetSearchPage(self):
        client = Client()

        response = client.get(reverse('MedicalStore:search'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(checkResponseHeaders(response))
