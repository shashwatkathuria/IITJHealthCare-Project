from django.db import models

# Create your models here.

class Doctor(models.Model):
    name = models.CharField(max_length = 30)
    address = models.CharField(max_length = 100)
    contactNumber = models.CharField(max_length = 10)
    email = models.CharField(max_length = 30)

    def __str__(self):
        return "Name : " + self.name + " Address : " + self.address + " Contact : " + self.contactNumber + " Email : " + self.email

class Patient(models.Model):
    name = models.CharField(max_length = 30)
    address = models.CharField(max_length = 100)
    contactNumber = models.CharField(max_length = 10)
    email = models.CharField(max_length = 30)

    def __str__(self):
        return "Name : " + self.name + " Address : " + self.address + " Contact : " + self.contactNumber + " Email : " + self.email

class Prescription(models.Model):
    prescriptionText = models.CharField(max_length = 2000)
    doctor = models.ForeignKey(Doctor, related_name = "doctorRecords", on_delete = models.CASCADE)
    patient = models.ForeignKey(Patient, related_name = "patientRecords", on_delete = models.CASCADE)

    def __str__(self):
        return "\nDoctor :" + str(self.doctor) + "\n\nPatient :" + str(self.patient) + "\n\nPrescription : \n\n" + self.prescriptionText + "\n\n"
