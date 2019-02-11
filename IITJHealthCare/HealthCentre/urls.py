from django.urls import path

from . import views

urlpatterns = [
    path('',views.index),
    path('register',views.register),
    path('doctors',views.doctors),
    path('login',views.login),
    path('emergency',views.emergency)
]
