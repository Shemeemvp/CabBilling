from django.urls import path
from CabApp import views

urlpatterns = [
    path('',views.loginPage, name='loginPage'),
    path('register',views.registerPage, name='registerPage'),
    path('trip_sheet',views.tripSheetPage, name='tripSheetPage'),
]