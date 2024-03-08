from django.shortcuts import render

# Create your views here.

def loginPage(request):
    return render(request, 'login.html')

def registerPage(request):
    return render(request, 'registration.html')

def tripSheetPage(request):
    return render(request, 'trip_sheet.html')