from django.conf.urls import url
from django.urls import path, re_path

from . import views

app_name = 'signup_login'

urlpatterns = [
    url(r'^signup/$', views.signup_view, name="signup"),
    url(r'login/$', views.login_view, name="login"),
    url(r'signup/patient$', views.patient_signup, name="patient"),
    url(r'signup/doctor$', views.doctor_signup, name="doctor"),
    url(r'logout/$', views.logout_view, name="logout"),
    re_path(r"^profile/(?P<username>[\w.@+-]+)", views.profile, name = "profile"),
    url(r'search/$', views.search, name="search"),


]