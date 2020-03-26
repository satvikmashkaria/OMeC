from django import forms
from .models import Doctor, Patient
from django.contrib.auth.models import User


class DoctorForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username', 'email','password')

class PatientForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username', 'email','password')

class DoctorSignUpForm(forms.ModelForm):
    # username = forms.CharField(max_length=30)
    firstname = forms.CharField(max_length=30)
    lastname = forms.CharField(max_length=30)
    # speciality = forms.CharField(max_length=20)
    phone_no = forms.IntegerField()
    address = forms.CharField(max_length=100)
    class Meta():
        model = Doctor
        fields = ('firstname', 'lastname', 'speciality', 'phone_no', 'address', 'image')

class PatientSignUpForm(forms.ModelForm):
    # username = forms.CharField(max_length=30)
    firstname = forms.CharField(max_length=30)
    lastname = forms.CharField(max_length=30)
    phone_no = forms.IntegerField()
    address = forms.CharField(max_length=100)
    class Meta():
        model = Patient
        fields = ('firstname', 'lastname', 'phone_no', 'address')

class SearchForm(forms.ModelForm):
    class Meta():
        model = Doctor
        fields = ('speciality',)
