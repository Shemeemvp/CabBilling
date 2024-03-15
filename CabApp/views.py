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
from datetime import date

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
                tollAmt = 0
                parkingAmt = 0
                entranceAmt = 0
                guideAmt = 0
                otherAmt = 0

                toll = request.POST.getlist('toll[]')
                parking = request.POST.getlist('parking[]')
                entrance = request.POST.getlist('entrance[]')
                guide_fee = request.POST.getlist('guide_fee[]')
                guide_place = request.POST.getlist('guide_place[]')
                other_charge = request.POST.getlist('other_charge_amount[]')
                other_charge_desc = request.POST.getlist('other_charge[]')
                
                print(guide_fee, guide_place)
                guide_fee_mapped = zip(guide_fee, guide_place)
                guide_fee_list = list(guide_fee_mapped)

                print(other_charge, other_charge_desc)
                other_charge_mapped = zip(other_charge, other_charge_desc)
                other_charge_list = list(other_charge_mapped)

                for t in toll:
                    try:
                        tollAmt += float(t)
                    except:
                        pass

                for p in parking:
                    try:
                        parkingAmt += float(p)
                    except:
                        pass
                
                for e in entrance:
                    try:
                        entranceAmt += float(e)
                    except:
                        pass

                for g in guide_fee:
                    try:
                        guideAmt += float(g)
                    except:
                        pass

                for o in other_charge:
                    try:
                        otherAmt += float(o)
                    except:
                        pass


                trip = TSC_Form(
                    user = usr,
                    driver = driver,
                    trip_no = trp_no,
                    trip_date = request.POST['trip_date'],
                    driver_name = request.POST['driver_name'],
                    guest = request.POST['guest_name'],
                    vehicle_no = request.POST['vehicle_number'],
                    vehicle_name = request.POST['vehicle_name'],
                    fixed_charge = request.POST['fixed_charge'],
                    extra_charge = request.POST['extra_charge'],
                    starting_km = request.POST['starting_kilometer'],
                    ending_km = request.POST['end_kilometer'],
                    trip_end_date = None if request.POST['trip_end_date'] == "" else request.POST['trip_end_date'],
                    starting_place = request.POST['starting_place'],
                    starting_time = request.POST['starting_time'],
                    destination = request.POST['destination'],
                    time_of_arrival = request.POST['time_of_arrival'],
                    kilometers = request.POST['kilometer'],
                    toll = tollAmt,
                    parking = parkingAmt,
                    entrance = entranceAmt,
                    guide_fee = guideAmt,
                    other_charges = otherAmt,
                    total_trip_expense = request.POST['total'],
                    advance = request.POST['advance'],
                    balance = request.POST['balance']
                )
                trip.save()

                for item in toll:
                    TSC_Expenses.objects.create(Trip = trip, exp_type = 'Toll', exp_desc = None, exp_amount = item, exp_date = date.today())

                for item in parking:
                    TSC_Expenses.objects.create(Trip = trip, exp_type = 'Parking', exp_desc = None, exp_amount = item, exp_date = date.today())
                
                for item in entrance:
                    TSC_Expenses.objects.create(Trip = trip, exp_type = 'Entrance', exp_desc = None, exp_amount = item, exp_date = date.today())

                for item in guide_fee_list:
                    TSC_Expenses.objects.create(Trip = trip, exp_type = 'Guide Fee', exp_desc = item[1], exp_amount = item[0], exp_date = date.today())

                for item in other_charge_list:
                    TSC_Expenses.objects.create(Trip = trip, exp_type = 'Other Charge', exp_desc = item[1], exp_amount = item[0], exp_date = date.today())

                # qr = qrcode.make("http://127.0.0.1:8000/trip/" + str(trip.id))
                qr = qrcode.make("http://127.0.0.1:8000/qr_details")

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
    if request.user.is_authenticated:
        trips = TSC_Form.objects.all().order_by('-id')
        context = {
            'trips': trips,
        }
        return render(request, 'all_trips.html',context)
    else:
        return redirect('/')
    
def viewTscData(request,id):
    if request.user.is_authenticated:
        tripData = TSC_Form.objects.get(id = id)
        context = {
            'trip': tripData,
        }
        return render(request, 'view_tsc_data.html',context)
    else:
        return redirect('/')
    
def qrDetails(request):
    return render(request, 'qr_landing.html')

def saveCustomerFeedback(request):
    name = request.GET['full_name']
    feedback = request.GET['feedback']
    Customer_Feedbacks.objects.create(full_name = name, feedback = feedback)
    messages.success(request, 'Thank you for your response')
    return redirect(qrDetails)

def getLastRideDetails(request):
    if request.user.is_authenticated:
        usr = User.objects.get(id = request.user.id)
        try:
            driver = Driver.objects.get(user = usr)
        except:
            driver = None

        trp = TSC_Form.objects.filter(user = usr).last()
        context = {
            'user':usr, 'driver':driver, 'trip':trp
        }
        print(trp)

        if not trp:
            messages.info(request, 'No Previous ride details exists.')
            return redirect(tripSheetPage)
        else:
            return render(request, 'previous_trip.html', context)
    else:
        return redirect('/')
    
def updateRide(request, id):
    if request.user.is_authenticated:
        try:
            if request.method == 'POST':
                usr = User.objects.get(id = request.user.id)
                try:
                    driver = Driver.objects.get(user = usr)
                except:
                    driver = None

                trip = TSC_Form.objects.get(id = id)
                trp_no = request.POST['trip_number']

                if trip.trip_no != trp_no and TSC_Form.objects.filter(trip_no__iexact = trp_no).exists():
                    res = f'<script>alert("Trip No. `{trp_no}` already exists.!");window.history.back();</script>'
                    return HttpResponse(res)
                else:
                    trip.trip_no = trp_no
                    trip.trip_date = request.POST['trip_date']
                    trip.driver_name = request.POST['driver_name']
                    trip.guest = request.POST['guest_name']
                    trip.vehicle_no = request.POST['vehicle_number']
                    trip.starting_place = request.POST['starting_place']
                    trip.starting_time = request.POST['starting_time']
                    trip.destination = request.POST['destination']
                    trip.time_of_arrival = request.POST['time_of_arrival']
                    trip.kilometers = request.POST['kilometer']
                    trip.toll = request.POST['toll']
                    trip.parking = request.POST['parking']
                    trip.entrance = request.POST['entrance']
                    trip.guide_fee = request.POST['guide_fee']
                    trip.advance = request.POST['advance']
                    trip.debit = request.POST['debit']
                    trip.balance = request.POST['balance']
                    trip.save()

                    messages.success(request, "Trip Updated successfully")
                    return redirect(tripSheetPage)
        except Exception as e:
            print(e)
            return redirect(tripSheetPage)
    else:
        return redirect('/')