from django.db import models

# Create your models here.

class Speciality(models.Model):
    spec = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.spec

class Doctor(models.Model):
    # doctor_id = models.IntegerField(primary_key=True)
    # email = models.CharField(max_length=40)
    username = models.CharField(max_length=30, primary_key=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    speciality = models.ForeignKey(Speciality, models.CASCADE, db_column='spec')
    phone_no = models.IntegerField()
    address = models.CharField(max_length=100)
    image = models.ImageField(null= True, blank= True)
    # password = models.CharField(max_length=100)

class Patient(models.Model):
    # patient_id = models.IntegerField(primary_key=True)
    # email = models.CharField(max_length=40)
    username = models.CharField(max_length=30, primary_key=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    phone_no = models.IntegerField()
    address = models.CharField(max_length=100)
    # password = models.CharField(max_length=100)
