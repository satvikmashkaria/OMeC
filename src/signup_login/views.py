from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Doctor, Patient, Speciality
from .forms import DoctorForm, PatientForm, DoctorSignUpForm, PatientSignUpForm, SearchForm
from django.db import IntegrityError

# Create your views here.


def signup_view(request):
    if request.method == 'POST':
        # print("heree", request.POST)
        if 'patient' in request.POST:
            return HttpResponseRedirect('/welcome/signup/patient')
        elif 'doctor' in request.POST:
            return HttpResponseRedirect('/welcome/signup/doctor')
    else:
        return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect('/messages')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})

def doctor_signup(request):
    reg = False
    email_in_use = False
    if request.method == 'POST':
        doc_form = DoctorForm(data = request.POST)
        doc_profile = DoctorSignUpForm(data = request.POST)
        if doc_form.is_valid() and doc_profile.is_valid():
            try:
                user = doc_form.save()
            except IntegrityError:
                # print("herweeeeeeeeeeeeeeeee")
                print(doc_form)
                email_in_use = True
                return render(request, 'doctor_signup.html', {'doc_form': doc_form, 'doc_profile': doc_profile, 'reg': reg, 'e': email_in_use})

            user.set_password(user.password)
            user.save()
            profile = doc_profile.save(commit=False)
            profile.user = user
            profile.username = user.username
            profile.save()
            reg = True
        else:
            print(doc_form.errors, doc_profile.errors)
    else:
        doc_form = DoctorForm()
        doc_profile = DoctorSignUpForm()
    
    return render(request, 'doctor_signup.html', {'doc_form': doc_form, 'doc_profile': doc_profile, 'reg': reg, 'e': email_in_use})

def patient_signup(request):
    reg = False
    email_in_use = False
    if request.method == 'POST':
        patient_form = PatientForm(data = request.POST)
        patient_profile = PatientSignUpForm(data = request.POST)
        if patient_form.is_valid() and patient_profile.is_valid():
            # print("hereeeeeeeeeeeeeeeeeeeee")
            try:
                user = patient_form.save()
            except IntegrityError:
                email_in_use = True
                return render(request, 'patient_signup.html', {'patient_form': patient_form, 'patient_profile': patient_profile, 'reg': reg, 'e': email_in_use})
            user.set_password(user.password)
            user.save()
            profile = patient_profile.save(commit=False)
            profile.user = user
            profile.username = user.username
            profile.save()
            reg = True
        else:
            print(patient_form.errors, patient_profile.errors)
    else:
        patient_form = PatientForm()
        patient_profile = PatientSignUpForm()
    
    return render(request, 'patient_signup.html', {'patient_form': patient_form, 'patient_profile': patient_profile, 'reg': reg, 'e': email_in_use })

def logout_view(request):
    user = request.user
    if user == None:
        print("Already logged out")
    else:
        logout(request)
    return redirect('signup_login:login')

def profile(request, username):
    print("username:", username)
    doc = Doctor.objects.get(username = username)

    return render(request, 'profile.html', {'doc' : doc})

def search(request):

    # if request.method == "GET":
    #     return render(request,"search.html",{})
    # else:
    if request.method == "POST":
        # print("aayu: ", request.POST)
        specname = request.POST.get('speciality')
        # print(specname)
        spec = Speciality.objects.get(spec = specname)
        docs = Doctor.objects.filter(speciality = spec)
        print(docs)
        search_form = SearchForm()
        return render(request,"search.html",{'search_form' : search_form, 'docs' : docs})


    else:
        search_form = SearchForm()
        return render(request,"search.html",{'search_form' : search_form})


def check_doctor(name):

    doc_l = Doctor.objects.filter(username = name)
    pat_l = Patient.objects.filter(username = name)

    if len(doc_l) > 0:
        return True
    elif len(pat_l) > 0:
        return False
    else:
        #Raise Error
        return False
