from django.db import models

# Create your models here.

class Doctor(models.Model):
    name = models.CharField(max_length = 30)
    address = models.CharField(max_length = 100)
    contactNumber = models.CharField(unique = True, max_length = 10)
    email = models.EmailField(unique = True, max_length = 255)

    def __str__(self):
        return "Name : " + self.name + " Address : " + self.address + " Contact : " + self.contactNumber + " Email : " + self.email

class Patient(models.Model):
    name = models.CharField(max_length = 30)
    address = models.CharField(max_length = 100)
    contactNumber = models.CharField(max_length = 10)
    rollNumber = models.CharField(unique = True, max_length = 8)
    email = models.EmailField(unique = True, max_length = 255)
    password = models.CharField(max_length = 64)

    def __str__(self):
        return "Name : " + self.name + " Address : " + self.address + " Contact : " + self.contactNumber + " Email : " + self.email

class Prescription(models.Model):
    prescriptionText = models.CharField(max_length = 2000)
    doctor = models.ForeignKey(Doctor, related_name = "doctorRecords", on_delete = models.CASCADE)
    patient = models.ForeignKey(Patient, related_name = "patientRecords", on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return "\nDoctor :" + str(self.doctor) + "\n\nPatient :" + str(self.patient) + "\n\nPrescription : \n\n" + self.prescriptionText + "\n\n"
