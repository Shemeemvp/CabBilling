from django.urls import path
from CabApp import views

urlpatterns = [
    path('',views.loginPage, name='loginPage'),
    path('register',views.registerPage, name='registerPage'),
    path('register_user',views.registerUser, name='registerUser'),
    path('trip_sheet',views.tripSheetPage, name='tripSheetPage'),
    path('user_login',views.userLogin, name='userLogin'),
    path('user_logout',views.userLogout, name='userLogout'),
    path('check_username',views.checkUserName, name='checkUserName'),
    path('check_phone_number',views.checkPhoneNumber, name='checkPhoneNumber'),
    path('end_current_trip',views.endCurrentTrip, name='endCurrentTrip'),
    path('all_trips',views.allTrips, name='allTrips'),
    path('view_tsc_data/<int:id>',views.viewTscData, name='viewTscData'),
    path('qr_details',views.qrDetails, name='qrDetails'),
]