from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
import qrcode
from django.conf import settings
import os
from django.core.files import File

# Create your views here.

def loginPage(request):
    return render(request, 'login.html')

def registerPage(request):
    return render(request, 'registration.html')

def tripSheetPage(request):
    if request.user.is_authenticated:
        usr = User.objects.get(id = request.user.id)
        try:
            driver = Driver.objects.get(user = usr)
        except:
            driver = None
        
        # Finding next Trip number w r t last Trip number if exists.
        nxtTRIP = ""
        lastTRIP = TSC_Form.objects.last()
        if lastTRIP:
            trip_no = str(lastTRIP.trip_no)
            numbers = []
            stri = []
            for word in trip_no:
                if word.isdigit():
                    numbers.append(word)
                else:
                    stri.append(word)
            
            num=''
            for i in numbers:
                num +=i
            
            st = ''
            for j in stri:
                st = st+j

            trp_num = int(num)+1

            if num[0] == '0':
                if trp_num <10:
                    nxtTRIP = st+'0'+ str(trp_num)
                else:
                    nxtTRIP = st+ str(trp_num)
            else:
                nxtTRIP = st+ str(trp_num)
        else:
            nxtTRIP = 'TRP01'
        
        context = {
            'user':usr, 'driver':driver, 'tripNo':nxtTRIP
        }
        return render(request, 'trip_sheet.html', context)
    else:
        return redirect('/')

def registerUser(request):
    try:
        if request.method == "POST":
            name = request.POST["full_name"]
            usrnm = request.POST["user_name"]
            phn = request.POST["mobile"]
            pswrd = request.POST["password"]

            if User.objects.filter(username=usrnm).exists():
                res = f'<script>alert("User name `{usrnm}` already exists, Please Login or try another.!");window.history.back();</script>'
                return HttpResponse(res)
            elif Driver.objects.filter(mobile__iexact = phn).exists():
                res = f'<script>alert("`{phn}` already exists, try another.!");window.history.back();</script>'
                return HttpResponse(res)
            else:
               userInfo = User.objects.create_user(
                username=usrnm,
                password=pswrd
            )
            userInfo.save()
            print("auth user saved...")
            dData = User.objects.get(id=userInfo.id)
            driverData = Driver(
                user=dData,
                full_name = name,
                mobile = phn
            )
            driverData.save()

            messages.success(request, 'Registration Successful..')
            return redirect(loginPage)
        else:
            return redirect(loginPage)
    except Exception as e:
        print(e)
        return redirect(loginPage)
    
def userLogin(request):
    if request.method == "POST":
        uName = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=uName, password=password)
        if user is not None:
            if user.is_staff:
                auth.login(request, user)
                return redirect(allTrips)
            else:
                auth.login(request, user)
                return redirect(tripSheetPage)
                    
        else:
            messages.error(request, "Incorrect Username or Password..Please try again")
            return redirect(loginPage)
    else:
        return redirect(loginPage)

def userLogout(request):
    logout(request)
    return redirect("/")

def checkUserName(request):
    if request.method == 'POST':
        uname = request.POST['username']
        print(uname)
        if User.objects.filter(username = uname).exists():
            return JsonResponse({'status':True, 'is_exists': True, 'message':'Username already Exists.!'})
        else:
            return JsonResponse({'status':True, 'is_exists': False, 'message':''})
    else:
        return redirect('/')

def checkPhoneNumber(request):
    if request.method == 'POST':
        phn = request.POST['phone']
        print(phn)
        if Driver.objects.filter(mobile__iexact = phn).exists():
            return JsonResponse({'status':True, 'is_exists': True, 'message':'Mobile No. already Exists.!'})
        else:
            return JsonResponse({'status':True, 'is_exists': False, 'message':''})
    else:
        return redirect('/')

def endCurrentTrip(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            usr = User.objects.get(id = request.user.id)
            try:
                driver = Driver.objects.get(user = usr)
            except:
                driver = None

            trp_no = request.POST['trip_number']

            if TSC_Form.objects.filter(trip_no__iexact = trp_no).exists():
                res = f'<script>alert("Trip No. `{trp_no}` already exists.!");window.history.back();</script>'
                return HttpResponse(res)
            else:
                trip = TSC_Form(
                    user = usr,
                    driver = driver,
                    trip_no = trp_no,
                    trip_date = request.POST['trip_date'],
                    driver_name = request.POST['driver_name'],
                    guest = request.POST['guest_name'],
                    vehicle_no = request.POST['vehicle_number'],
                    starting_place = request.POST['starting_place'],
                    starting_time = request.POST['starting_time'],
                    destination = request.POST['destination'],
                    time_of_arrival = request.POST['time_of_arrival'],
                    kilometers = request.POST['kilometer'],
                    toll = request.POST['toll'],
                    parking = request.POST['parking'],
                    entrance = request.POST['entrance'],
                    guide_fee = request.POST['guide_fee'],
                    advance = request.POST['advance'],
                    debit = request.POST['debit'],
                    balance = request.POST['balance']
                )
                trip.save()
                qr = qrcode.make("http://127.0.0.1:8000/trip/" + str(trip.id))

                image_directory = os.path.join(settings.MEDIA_ROOT, "images")
                if not os.path.exists(image_directory):
                    os.makedirs(image_directory)
                image_path = os.path.join(settings.MEDIA_ROOT, "images", "trip" + str(trip.id) + ".png")
                qr.save(image_path)
                with open(image_path, "rb") as reopen:
                    djangofile = File(reopen)
                    trip.bill_qr = djangofile
                    trip.save()

                messages.success(request, "Trip Ended successfully")
                return redirect(tripSheetPage)
    else:
        return redirect('/')
    
def allTrips(request):
    if request.user.is_authenticated and request.user.is_staff:
        trips = TSC_Form.objects.all().order_by('-id')
        context = {
            'trips': trips,
        }
        return render(request, 'all_trips.html',context)
    else:
        return redirect('/')
    
def viewTscData(request,id):
    if request.user.is_authenticated and request.user.is_staff:
        tripData = TSC_Form.objects.get(id = id)
        context = {
            'trip': tripData,
        }
        return render(request, 'view_tsc_data.html',context)
    else:
        return redirect('/')