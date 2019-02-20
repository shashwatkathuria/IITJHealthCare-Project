from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = "index"),
    path('register', views.register, name = "register"),
    path('doctors', views.doctors, name = "doctors"),
    path('login', views.login, name = "login"),
    path('emergency', views.emergency, name = "emergency"),
    path('logout', views.logout, name = "logout"),
    path('contactus', views.contactus, name = "contactus"),
    path('onlineprescription', views.onlineprescription, name = "onlineprescription")
]
