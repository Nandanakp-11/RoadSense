from datetime import timedelta

from django.db.models import F, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
# from haversine import Unit, haversine
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from haversine import haversine, Unit
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from myapp.models import *


def login(request):
    return render(request,'Login.html')
def login_post(request):
    username=request.POST["username"]
    password=request.POST["password"]
    obj=Login.objects.filter(username=username,password=password)
    print(username,password)
    if obj.exists():
        obj=Login.objects.get(username=username,password=password)
        if obj.type=='Admin':
            request.session['lid']=obj.id
            return redirect('/myapp/Admin_home/')
            # return HttpResponse('''<script>alert('login successfully');window.location='/myapp/Admin_home/'</script>''')
        elif obj.type=='Evstation':
            request.session['lid']=obj.id
            return redirect('/myapp/Evstnhome/')

            # return HttpResponse('''<script>alert('login successfully');window.location='/myapp/Evstnhome/'</script>''')
        elif obj.type=='Fuelstation':
            request.session['lid']=obj.id
            return redirect('/myapp/fs_home/')

            # return HttpResponse('''<script>alert('login successfully');window.location='/myapp/fs_home/'</script>''')
    return HttpResponse('''<script>alert('Invalid username or password');window.location='/myapp/login/'</script>''')

def logout(request):
    request.session['lid']=''
    return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

def change_password(request):
    res=Login.objects.get(id=request.session['lid'])
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    return render(request, 'Admin/Change password.html', {'data':res})
def change_pswd_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    pass1 = request.POST["textfield"]
    pass2 = request.POST["textfield2"]
    pass3 = request.POST["textfield3"]
    obj = Login.objects.get(id=request.session['lid'])
    # #print(pass1)
    # #print(obj.password)
    if obj.password == pass1:
        obj.password = pass2
        obj.save()
        return HttpResponse("<script>alert('You changed password');window.location='/myapp/login/'</script>")
    else:
        return HttpResponse(
            "<script>alert('You cannot change password!!!!!!!!!!!!');window.location='/myapp/change_password/'</script>")

def Admin_home(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    return render(request,'Admin/Adminindexhome.html')

def manage_evStations(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    res=Evstation.objects.filter(status='pending')
    return render(request,'Admin/managestations.html',{'data':res})
def search_Ev(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    srch=request.POST["search"]
    res=Evstation.objects.filter(stationname__icontains=srch,status='pending')

    return render(request,'Admin/managestations.html',{'data':res})
def Approve_ev(request,did):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    res=Evstation.objects.filter(LOGIN=did).update(status='Approved')
    res=Login.objects.filter(id=did).update(type='Evstation')

    return HttpResponse("<script>alert('You Approved the Evstation');window.location='/myapp/manage_ev/'</script>")
def Approved_stations(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    res=Evstation.objects.filter(status='Approved')
    return render(request,'Admin/view_Approved_stations.html',{'data':res})
def Search_Apprved_ev(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    srch = request.POST["search"]
    res = Evstation.objects.filter(stationname__icontains=srch,status='Approved')
    return render(request, 'Admin/view_Approved_stations.html', {'data': res})
def Reject_ev(request,did):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    res=Evstation.objects.filter(id=did).update(status='Rejected')
    return HttpResponse("<script>alert('You Rejected the Evstation');window.location='/myapp/manage_ev/'</script>")
def RejectedStations(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    res=Evstation.objects.filter(status='Rejected')
    return render(request,'Admin/view_Rejected_stations.html',{'data':res})
def Search_Rjctd_ev(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    srch = request.POST["search"]
    res = Evstation.objects.filter(stationname__icontains=srch,status='Rejected')
    return render(request, 'Admin/view_Rejected_stations.html', {'data': res})




def manage_workers(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')
    res=Workers.objects.filter(status='Pending')
    return render(request,'Admin/manage_workers.html',{'data':res})
def Search_workers(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    srch = request.POST["search"]
    res = Workers.objects.filter(wname__icontains=srch,status='Pending')
    return render(request, 'Admin/manage_workers.html', {'data': res})
def verify_worker(request,did):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    res=Workers.objects.filter(LOGIN_id=did).update(status='Verified')
    Login.objects.filter(id=did).update(type='Worker')
    return HttpResponse("<script>alert('You Verified the Worker');window.location='/myapp/manage_workers/'</script>")
def verifyed_workers(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    res=Workers.objects.filter(status='Verified')
    return render(request,'Admin/View_verified_workers.html',{'data':res})

def Search_vrfyd_workers(request):
    srch = request.POST["search"]
    res = Workers.objects.filter(wname__icontains=srch,status='Verified')
    return render(request, 'Admin/View_verified_workers.html', {'data': res})

def reject_worker(request,did):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    res=Workers.objects.filter(id=did).update(status='Rejected')
    return HttpResponse("<script>alert('You Rejected the Worker');window.location='/myapp/manage_workers/'</script>")
def Rejected_workers(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    res=Workers.objects.filter(status='Rejected')
    return render(request,'Admin/View_rejected_workers.html',{'data':res})
def Search_Rjctd_workers(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    srch = request.POST["search"]
    res = Workers.objects.filter(wname__icontains=srch,status='Rejected')
    return render(request, 'Admin/View_rejected_workers.html', {'data': res})

def view_fuel_station(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    res=Fuelstation.objects.filter(status='Pending')
    return render(request,'Admin/view_fuel_station.html',{'data':res})

def view_fuel_station_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    srch = request.POST["search"]
    res = Fuelstation.objects.filter(stationname__icontains=srch,status='Pending')
    return render(request,'Admin/view_fuel_station.html',{'data':res})

def Approve_fuel(request,did):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    res=Fuelstation.objects.filter(LOGIN=did).update(status='Approved')
    res=Login.objects.filter(id=did).update(type='Fuelstation')
    return HttpResponse("<script>alert('You Approved the Fuelstation');window.location='/myapp/view_fuel_station/'</script>")

def Approved_fuel_stations(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    res=Fuelstation.objects.filter(status='Approved')
    return render(request,'Admin/view_Approved_fuel_stations.html',{'data':res})
def Approved_fuel_stations_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    srch = request.POST["search"]
    res = Fuelstation.objects.filter(stationname__icontains=srch,status='Approved')
    return render(request,'Admin/view_Approved_fuel_stations.html',{'data':res})
def Reject_fuel(request,did):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    res=Fuelstation.objects.filter(id=did).update(status='Rejected')
    return HttpResponse("<script>alert('You Rejected the Fuelstation');window.location='/myapp/view_fuel_station/'</script>")
def Rejected_fuel_Stations(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    res=Fuelstation.objects.filter(status='Rejected')
    return render(request,'Admin/view_Rejected_fuel_stations.html',{'data':res})
def Rejected_fuel_Stations_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    srch = request.POST["search"]
    res = Fuelstation.objects.filter(stationname__icontains=srch,status='Rejected')
    return render(request,'Admin/view_Rejected_fuel_stations.html',{'data':res})

def view_user_complaint_nd_reply(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    res=Complaints.objects.all()
    return render(request,'Admin/View_user_complaint_nd_reply.html',{'data':res})
def Search_User_comp(request):
    if request.session['lid']=='':
         return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    fromd= request.POST["fromdate"]
    tod=request.POST["fromdate"]
    res = Complaints.objects.filter(date__range=[fromd,tod])
    return render(request, 'Admin/View_user_complaint_nd_reply.html', {'data': res})
def reply_user_com(request,did):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    res=Complaints.objects.get(id=did)
    return render(request,'Admin/Send_reply_user.html',{'data':res})
def send_reply_post_user(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    did=request.POST["did"]
    reply=request.POST["reply"]
    obj=Complaints.objects.get(id=did)
    obj.reply=reply
    obj.status='Replyed'
    obj.save()
    return HttpResponse("<script>alert('You Replyed to User Successfully');window.location='/myapp/view_user_complaint_nd_reply/'</script>")

def view_review_rating(request):
    if request.session['lid'] == '':
        return HttpResponse('Login Required')
    else:
        res=Review_app.objects.all()
        return render(request,'Admin/view_app_review.html',{'data':res})

def view_review_rating_post(request):
    if request.session['lid'] == '':
        return HttpResponse('Login Required')
    else:
        fdate=request.POST['textfield']
        tdate=request.POST['textfield2']
        res=Review_app.objects.filter(date__range=[fdate,tdate])
        return render(request,'Admin/view_app_review.html',{'data':res})



#=============Ev station==============

def home(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    return render(request,"Evstation/EvstationHomeindex.html")


def signin(request):
    return render(request,"Evstation/Regindex.html")
def Signin_post(request):
    name=request.POST["evstn"]
    licno=request.POST["licno"]
    phn=request.POST["phone"]
    mail=request.POST["mail"]
    passwd=request.POST["passwd"]
    place=request.POST["place"]
    district=request.POST["district"]
    state=request.POST["state"]
    pincode=request.POST["pincode"]
    lat=request.POST["latitude"]
    longi=request.POST["longitude"]
    ob=Login()
    ob.username=mail
    ob.password=passwd
    ob.type="Pending"
    ob.save()
    obj=Evstation()
    obj.stationname=name
    obj.licenseno=licno
    obj.phone=phn
    obj.email=mail
    obj.place=place
    obj.district=district
    obj.state=state
    obj.pincode=pincode
    obj.latitude=lat
    obj.longitude=longi
    obj.LOGIN_id=ob.id
    obj.status="Pending"
    obj.save()
    return HttpResponse("<script>alert('Registered successfully. Your verification is processing… Please wait for the confirmation.');window.location='/myapp/login/'</script>")

def ev_profile(request):
    re=Evstation.objects.get(LOGIN_id=request.session['lid'])
    return render(request,'Evstation/view profile.html',{'i':re})

def ed_edit_profile(request):
    re=Evstation.objects.get(LOGIN_id=request.session['lid'])
    return render(request,'Evstation/edit_profile.html',{'i':re})

def ed_edit_profile_post(request):
    name = request.POST["evstn"]
    licno = request.POST["licno"]
    phn = request.POST["phone"]
    mail = request.POST["mail"]
    place = request.POST["place"]
    district = request.POST["district"]
    state = request.POST["state"]
    pincode = request.POST["pincode"]
    ob = Login.objects.get(id=request.session['lid'])
    ob.username = mail
    ob.save()
    obj = Evstation.objects.get(LOGIN_id=request.session['lid'])
    obj.stationname = name
    obj.licenseno = licno
    obj.phone = phn
    obj.email = mail
    obj.place = place
    obj.district = district
    obj.state = state
    obj.pincode = pincode
    obj.save()
    return HttpResponse("<script>alert('Updated successfully...');window.location='/myapp/ev_profile/'</script>")




def change_password_ev(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    res = Login.objects.get(id=request.session['lid'])
    return render(request, 'Evstation/change password.html', {'data': res})

def change_pswd_post_ev(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    pass1 = request.POST["textfield"]
    pass2 = request.POST["textfield2"]
    pass3 = request.POST["textfield3"]
    obj = Login.objects.get(id=request.session['lid'])

    if obj.password == pass1:
        obj.password = pass2
        obj.save()
        return HttpResponse("<script>alert('You changed password');window.location='/myapp/login/'</script>")
    else:
       return HttpResponse("<script>alert('You cannot change password!!!!!!!!!!!!');window.location='/myapp/change_password_ev/'</script>")

def add_charging_point(request):
    return render(request,'Evstation/Add charging point.html')


def add_charging_point_post(request):
    speed=request.POST['speed']
    outlettype=request.POST['type']
    number_of_outlets=request.POST['outlet']
    Price=request.POST['price']
    c=Charging_point()
    c.speed=speed
    c.outlettype=outlettype
    c.number_of_outlets=number_of_outlets
    c.Price=Price
    c.EV=Evstation.objects.get(LOGIN_id=request.session['lid'])
    c.save()
    return HttpResponse(
        "<script>alert('Added..Sucessfully...');window.location='/myapp/add_charging_point/'</script>")


def view_charging_point(request):
    re=Charging_point.objects.filter(EV__LOGIN_id=request.session['lid'])
    return render(request,'Evstation/view charging point.html',{'data':re})


def view_charging_point_post(request):
    s=request.POST['from']
    re = Charging_point.objects.filter(EV__LOGIN_id=request.session['lid'],speed__contains=s)
    return render(request, 'Evstation/view charging point.html', {'data': re})


def edit_charging_point(request,id):
    re=Charging_point.objects.get(id=id)
    return render(request,'Evstation/edid charging point.html',{'data':re})

def edit_charging_point_post(request):
    id=request.POST['id']
    speed = request.POST['speed']
    outlettype = request.POST['type']
    number_of_outlets = request.POST['outlet']
    Price = request.POST['price']
    c = Charging_point.objects.get(id=id)
    c.speed = speed
    c.outlettype = outlettype
    c.number_of_outlets = number_of_outlets
    c.Price = Price
    c.save()
    return HttpResponse(
        "<script>alert('updated..Sucessfully...');window.location='/myapp/view_charging_point/'</script>")

def delete_charging_point(request,id):
    Charging_point.objects.filter(id=id).delete()
    return redirect('/myapp/view_charging_point/')


def Addslot(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')
    from datetime import datetime
    date=datetime.now().today()
    res=Charging_point.objects.filter(EV__LOGIN_id=request.session['lid'])
    return render(request,"Evstation/Add Slot.html",{'data':res,'date':date})
def Addslot_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    charge=request.POST["charge"]
    date=request.POST["date"]
    slo=request.POST["slots"]
    obj=Slots()
    obj.CHARGINGPOINT=Charging_point.objects.get(id=charge)
    obj.date=date
    obj.slots=slo
    obj.save()
    return HttpResponse("<script>alert('You Added a Slot...');window.location='/myapp/Addslot/'</script>")
def View_slot(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    res=Slots.objects.filter(CHARGINGPOINT__EV__LOGIN_id=request.session['lid']).order_by('-id')
    return render(request,"Evstation/view slot.html",{'data':res})
def Search_slots(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    fromd = request.POST["from"]
    tod = request.POST["to"]
    res = Slots.objects.filter(date__range=[fromd, tod],CHARGINGPOINT__EV__LOGIN_id=request.session['lid'])
    return render(request,"Evstation/view slot.html",{'data':res})
def delete_slot(request,did):
    res=Slots.objects.filter(id=did).delete()
    return redirect('/myapp/View_slot/')
def edit_slot(request,did):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    from datetime import datetime
    date = datetime.now().today()
    res=Slots.objects.get(id=did)
    mm=Charging_point.objects.filter(EV__LOGIN_id=request.session['lid'])
    return render(request,"Evstation/Edit slot.html",{'data':res,'data1':mm,'dat':date})
def Edit_slot_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    charge = request.POST["charge"]
    date = request.POST["date"]
    slo = request.POST["slots"]
    did=request.POST["id1"]
    obj = Slots.objects.get(id=did)
    obj.CHARGINGPOINT = Charging_point.objects.get(id=charge)
    obj.date = date
    obj.slots = slo
    obj.save()
    return HttpResponse("<script>alert('You Updated a Slot...');window.location='/myapp/View_slot/'</script>")
def view_slot_booked(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    res=Slotbooking.objects.filter(SLOTS__CHARGINGPOINT__EV__LOGIN_id=request.session['lid'])
    return render(request,"Evstation/view_slot_booking.html",{'data':res})
def approve_slots(request,did):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    res=Slotbooking.objects.filter(id=did).update(status='Approved')
    return HttpResponse("<script>alert('You Verified the Worker');window.location='/myapp/view_slot_booked/'</script>")

def reject_slots(request,did):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    res=Slotbooking.objects.filter(id=did).update(status='Rejected')
    return HttpResponse("<script>alert('You Verified the Worker');window.location='/myapp/view_slot_booked/'</script>")
def Search_booked_slots(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    fromd = request.POST["from"]
    tod = request.POST["to"]
    res = Slotbooking.objects.filter(SLOTS__date__range=[fromd, tod],SLOTS__EVSTATIONS__LOGIN_id=request.session['lid'])
    return render(request,'Evstation/view_slot_booking.html',{'data':res})
def View_Approved_slots(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')
    res=Slotbooking.objects.filter(status='Approved')
    return render(request,"Evstation/view_approved_slots.html",{'data':res})
def Approved_slot_search(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    fromd = request.POST["from"]
    tod = request.POST["to"]
    res = Slotbooking.objects.filter(SLOTS__date__range=[fromd, tod],status='Approved')
    return render(request,"Evstation/view_approved_slots.html",{'data':res})
def View_Rejected_slots(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    res=Slotbooking.objects.filter(status='Rejected')
    return render(request,"Evstation/view_rejected_slots.html",{'data':res})
def Rejected_slot_search(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    fromd = request.POST["from"]
    tod = request.POST["to"]
    res = Slotbooking.objects.filter(SLOTS__date__range=[fromd, tod],status='Rejected')
    return render(request,"Evstation/view_rejected_slots.html",{'data':res})
def View_users(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    res=Users.objects.all()
    return render(request,'Evstation/view_users.html',{'data':res})
def search_view_users(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    srch=request.POST["search"]
    res=Users.objects.filter(uname__icontains=srch)
    return render(request,'Evstation/view_users.html',{'data':res})

def ev_view_booking(request,id):
    request.session['slotid']=id
    re=Slotbooking.objects.filter(SLOTS_id=id).order_by('-id')
    return render(request,'Evstation/view_slot_booking.html',{'data':re})


def ev_view_booking_post(request):
    fromd = request.POST["from"]
    tod = request.POST["to"]
    re = Slotbooking.objects.filter(SLOTS_id=request.session['slotid'],date__range=[fromd,tod]).order_by('-id')
    return render(request, 'Evstation/view_slot_booking.html', {'data': re})

def ev_view_payment(request):
    re=Payment.objects.filter(SLOTBOOKING__SLOTS__CHARGINGPOINT__EV__LOGIN_id=request.session['lid'])
    return render(request,'Evstation/view_payment.html',{'data':re})

def ev_view_payment_post(request):
    fromd = request.POST["from"]
    tod = request.POST["to"]
    re=Payment.objects.filter(SLOTBOOKING__SLOTS__CHARGINGPOINT__EV__LOGIN_id=request.session['lid'],date__range=[fromd,tod])
    return render(request,'Evstation/view_payment.html',{'data':re})


def ev_view_review(request):
    re=Ev_Review.objects.filter(EV__LOGIN_id=request.session['lid'])
    return render(request,'Evstation/view_user_feedback.html',{'data':re})


def ev_view_review_post(request):
    fromd=request.POST['from']
    tod=request.POST['to']
    re = Ev_Review.objects.filter(EV__LOGIN_id=request.session['lid'],date__range=[fromd,tod])
    return render(request, 'Evstation/view_user_feedback.html', {'data': re})

def view_user_feedback(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    lid=request.session['lid']
    res=Ev_Review.objects.filter(EVSTATIONS__LOGIN_id=lid)
    return render(request,"Evstation/view_user_feedback.html",{'data':res})
def Search_user_feed(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    lid=request.session['lid']
    fromd = request.POST["from"]
    tod = request.POST["to"]
    res = Ev_Review.objects.filter(date__range=[fromd, tod],EVSTATIONS__LOGIN_id=lid)
    return render(request,"Evstation/view_user_feedback.html",{'data':res})


#===========Fuel Station===================

def fs_email_exist(request):
    email = request.POST['email']

    status = Fuelstation.objects.filter(email = email).exists()

    return JsonResponse({'status':status})

def f_register(request):
    return render(request,"Fstation/Regindex.html")
def f_register_post(request):
    name=request.POST["evstn"]
    licno=request.POST["licno"]
    phn=request.POST["phone"]
    mail=request.POST["mail"]
    passwd=request.POST["passwd"]
    place=request.POST["place"]
    district=request.POST["district"]
    state=request.POST["state"]
    pincode=request.POST["pincode"]
    lat = request.POST["latitude"]
    longi = request.POST["longitude"]
    ob=Login()
    ob.username=mail
    ob.password=passwd
    ob.type="Pending"
    ob.save()
    obj=Fuelstation()
    obj.stationname=name
    obj.licenseno=licno
    obj.phone=phn
    obj.email=mail
    obj.place=place
    obj.district=district
    obj.state=state
    obj.pincode=pincode
    obj.latitude=lat
    obj.longitude=longi
    obj.LOGIN_id=ob.id
    obj.status="Pending"
    obj.save()
    return HttpResponse("<script>alert('Registered successfully. Your verification is processing… Please wait for the confirmation.');window.location='/myapp/login/'</script>")

def fs_home(request):
    re = Work_status.objects.filter(FUEL__LOGIN_id=request.session['lid'])
    from datetime import datetime
    date = datetime.now().today()
    if re.exists():
        Work_status.objects.filter(FUEL__LOGIN_id=request.session['lid']).update(status='pending', date=date)
        return render(request, 'Fstation/Homeindex.html')


    else:
        re = Work_status()
        re.status = 'pending'
        re.date = date
        re.FUEL = Fuelstation.objects.get(LOGIN_id=request.session['lid'])
        re.save()
    return render(request,'Fstation/Homeindex.html')


def fs_profile(request):
    re=Fuelstation.objects.get(LOGIN_id=request.session['lid'])
    ree=Work_status.objects.get(FUEL__LOGIN_id=request.session['lid'])
    return render(request,'Fstation/view profile.html',{'i':re,'data':ree})

def active_work_status(request,id):
    # re=Work_status.objects.filter(FUEL__LOGIN_id=id)
    # if re.exists():
    from datetime import datetime
    date=datetime.now().today()
    Work_status.objects.filter(FUEL__LOGIN_id=id).update(status='active',date=date)
    return redirect('/myapp/fs_profile/')

def deactive_work_status(request,id):
    from datetime import datetime
    date = datetime.now().today()
    Work_status.objects.filter(FUEL__LOGIN_id=id).update(status='pending', date=date)
    return redirect('/myapp/fs_profile/')



def fs_edit_profile(request):
    re=Fuelstation.objects.get(LOGIN_id=request.session['lid'])
    return render(request,'Fstation/edit_profile.html',{'i':re})

def fs_edit_profile_post(request):
    name = request.POST["evstn"]
    licno = request.POST["licno"]
    phn = request.POST["phone"]
    mail = request.POST["mail"]
    place = request.POST["place"]
    district = request.POST["district"]
    state = request.POST["state"]
    pincode = request.POST["pincode"]
    ob = Login.objects.get(id=request.session['lid'])
    ob.username = mail
    ob.save()
    obj = Fuelstation.objects.get(LOGIN_id=request.session['lid'])
    obj.stationname = name
    obj.licenseno = licno
    obj.phone = phn
    obj.email = mail
    obj.place = place
    obj.district = district
    obj.state = state
    obj.pincode = pincode
    obj.save()
    return HttpResponse("<script>alert('Updated successfully...');window.location='/myapp/fs_profile/'</script>")

def fs_add_stock(request):
    return render(request,'Fstation/Add fuel_stock.html')


def fs_add_stock_post(request):
    fuel=request.POST['charge']
    brand=request.POST['brand']
    qty=request.POST['quantity']
    prce=request.POST['price']
    stock=request.POST['stock']
    re=Fuel_Stock.objects.filter(FUEL__LOGIN_id=request.session['lid'],fuel_type=fuel,brand=brand,quantity=qty)
    if re.exists():
        Fuel_Stock.objects.filter(FUEL__LOGIN_id=request.session['lid'],fuel_type=fuel,brand=brand,quantity=qty).update(stock=F('stock')+stock)
        return HttpResponse("<script>alert('Updated successfully...');window.location='/myapp/fs_add_stock/'</script>")

    ss=Fuel_Stock()
    ss.FUEL=Fuelstation.objects.get(LOGIN_id=request.session['lid'])
    ss.fuel_type=fuel
    ss.brand=brand
    ss.quantity=qty
    ss.price=prce
    ss.stock=stock
    ss.save()
    return HttpResponse("<script>alert('Added successfully...');window.location='/myapp/fs_add_stock/'</script>")


def fs_view_stock(request):
    re=Fuel_Stock.objects.filter(FUEL__LOGIN_id=request.session['lid'])
    return render(request,'Fstation/view fuel_stock.html',{'data':re})

def fs_view_stock_post(request):
    s=request.POST['from']
    re = Fuel_Stock.objects.filter(FUEL__LOGIN_id=request.session['lid'],fuel_type__icontains=s)
    return render(request, 'Fstation/view fuel_stock.html', {'data': re})


def fs_delete_stock(request,id):
    Fuel_Stock.objects.filter(id=id).delete()
    return redirect('/myapp/fs_view_stock/')



def fs_view_bookings(request):
    re=Fuel_Booking.objects.filter(FUEL_STOCK__FUEL__LOGIN_id=request.session['lid']).order_by('-id')
    l=[]
    for i in re:
        lat=Location.objects.get(LOGIN_id=i.USER.LOGIN.id).latitude
        longi=Location.objects.get(LOGIN_id=i.USER.LOGIN.id).longitude

        l.append({
            'id':i.id,
            'date':i.date,
            'fuel_type':i.FUEL_STOCK.fuel_type,
            'brand':i.FUEL_STOCK.brand,
            'quantity':i.FUEL_STOCK.quantity,
            'price':i.FUEL_STOCK.price,
            'uname':i.USER.uname,
            'email':i.USER.email,
            'phone':i.USER.phone,
            'lat':lat,
            'long':longi
        })
    return render(request,'Fstation/view_fuel_booking.html',{'data':l})


def fs_view_review(request):
    re=Fs_Review.objects.filter(FS__LOGIN_id=request.session['lid'])
    return render(request,'Fstation/view_user_review.html',{'data':re})

def fs_view_review_post(request):
    fd=request.POST['from']
    td=request.POST['to']
    re=Fs_Review.objects.filter(FS__LOGIN_id=request.session['lid'],date__range=[fd,td])
    return render(request,'Fstation/view_user_review.html',{'data':re})




def fs_change_password(request):
    res=Login.objects.get(id=request.session['lid'])
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    return render(request, 'Admin/Change password.html', {'data':res})
def fs_change_pswd_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('You  Logout Successfully');window.location='/myapp/login/'</script>''')

    pass1 = request.POST["textfield"]
    pass2 = request.POST["textfield2"]
    pass3 = request.POST["textfield3"]
    obj = Login.objects.get(id=request.session['lid'])
    # #print(pass1)
    # #print(obj.password)
    if obj.password == pass1:
        obj.password = pass2
        obj.save()
        return HttpResponse("<script>alert('You changed password');window.location='/myapp/login/'</script>")
    else:
        return HttpResponse(
            "<script>alert('You cannot change password!!!!!!!!!!!!');window.location='/myapp/fs_change_password/'</script>")



#==============Worker===========================================



def and_login(request):
    user = request.POST['username']
    password = request.POST['password']
    print(password,user)
    res = Login.objects.filter(username=user, password=password)
    #print(request.POST)
    if res.exists():
        ress = Login.objects.get(username=user, password=password)
        lid = ress.id
        if ress.type == "Worker":
            return JsonResponse({'status': 'ok', 'lid': str(lid),'type':ress.type})
        elif ress.type == "user":
            u=Users.objects.get(LOGIN_id=lid)
            return JsonResponse({'status': 'ok','lid': str(lid),'type':ress.type,'name':u.uname,'uemail':u.email,'photo':u.photo})
        else:
            return JsonResponse({'status': 'no'})
    else:
        return JsonResponse({'status': 'no'})



def worker_signup_post(request):
    name=request.POST['name']
    dob=request.POST['dob']
    gender=request.POST['gender']
    email=request.POST['email']
    phone=request.POST['phone']
    place=request.POST['place']
    expr=request.POST['expr']
    district=request.POST['district']
    quali=request.POST['qualification']
    photo=request.POST['photo']
    state=request.POST['state']

    import datetime
    import base64
    #
    date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    a = base64.b64decode(photo)
    fh = open("C:\\Users\\asus\\PycharmProjects\\road sense\\road_sense\\media\\worker_photo\\" + date + ".jpg", "wb")
    path = "/media/worker_photo/" + date + ".jpg"
    fh.write(a)
    fh.close()


    certifi = request.POST['certificate']
    date1 = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    a1 = base64.b64decode(certifi)
    fh = open("C:\\Users\\asus\\PycharmProjects\\road sense\\road_sense\\media\\" + date1 + "2.jpg", "wb")
    # fh = open("C:\\Users\\91815\\PycharmProjects\\cyber\\media\\" + date + ".jpg", "wb")
    path2 = "/media/" + date1 + "2.jpg"
    fh.write(a1)
    fh.close()



    # fs=FileSystemStorage()
    # fn=fs.save(date,photo)
    # path=fs.url(date)
    password = request.POST['password']
    cpassword = request.POST['cpassword']

    dd=Workers.objects.filter(email=email)
    if dd.exists():
        return JsonResponse({'status': 'no'})

    lobj = Login()
    lobj.username = email
    lobj.password = cpassword
    lobj.type = 'pending'
    lobj.save()

    uobj = Workers()
    uobj.wname = name
    uobj.email = email
    uobj.gender = gender
    uobj.phone = phone
    uobj.email = email
    uobj.experience = expr
    uobj.dob = dob
    uobj.photo = path
    uobj.qualification = quali
    uobj.certificate = path2
    uobj.place = place
    uobj.district = district
    uobj.state = state
    uobj.LOGIN = lobj
    uobj.status = 'pending'
    uobj.save()
    return JsonResponse({'status': 'ok'})



def worker_view_profile(request):
    lid = request.POST['lid']
    res = Workers.objects.get(LOGIN=lid)
    #print(res)
    return JsonResponse({'status': 'ok', 'name': res.wname,
                         'email': res.email, 'phone': res.phone,
                         'gender':res.gender,
                         'dob': res.dob, 'photo': res.photo,
                         'proof': res.certificate,'place': res.place,
                         'state': res.state,
                         'experience': res.experience,
                         'district': res.district,
                         'qualification':res.qualification,
                         'login':res.LOGIN.id})




def worker_edit_profile(request):
    lid = request.POST['lid']
    name = request.POST['name']
    dob = request.POST['dob']
    gender = request.POST['gender']
    email = request.POST['email']
    phone = request.POST['phone']
    place = request.POST['place']
    expr = request.POST['expr']
    district = request.POST['district']
    quali = request.POST['qualification']
    photo = request.POST['photo']
    state = request.POST['state']
    certifi = request.POST['certificate']

    Login.objects.filter(id=lid).update(username=email)

    uobj = Workers.objects.get(LOGIN=lid)


    uobj.wname = name
    uobj.email = email
    uobj.gender = gender
    uobj.phone = phone
    uobj.email = email
    uobj.experience = expr
    uobj.dob = dob
    uobj.qualification = quali
    uobj.place = place
    uobj.district = district
    uobj.state = state
    if len(photo)!=0:
        import datetime
        import base64
        #
        date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        a = base64.b64decode(photo)
        fh = open("C:\\road_sense\\media\\worker_photo\\" + date + ".jpg", "wb")
        # fh = open("C:\\Users\\91815\\PycharmProjects\\cyber\\media\\" + date + ".jpg", "wb")
        path = "/media/worker_photo/" + date + ".jpg"
        fh.write(a)
        fh.close()
        uobj.photo = path

    if len(certifi)!=0:
        import datetime
        import base64
        date1 = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        a1 = base64.b64decode(certifi)
        fh = open("C:\\road_sense\\media\\" + date1 + "2.jpg", "wb")
        # fh = open("C:\\Users\\91815\\PycharmProjects\\cyber\\media\\" + date + ".jpg", "wb")
        path2 = "/media/" + date1 + "2.jpg"
        fh.write(a1)
        fh.close()

        uobj.certificate = path2


    uobj.save()
    return JsonResponse({'status': 'ok'})



def w_add_service(request):
    lid=request.POST['lid']
    name=request.POST['name']
    charge=request.POST['price']
    w=Worker_Service()
    w.WORKER=Workers.objects.get(LOGIN_id=lid)
    w.name=name
    w.charge=charge
    w.save()
    return JsonResponse({'status': 'ok'})



def w_view_service(request):
    lid=request.POST['lid']
    re=Worker_Service.objects.filter(WORKER__LOGIN_id=lid)
    l=[]
    for i in re:
        l.append({
            'id':i.id,
            'name':i.name,
            'price':i.charge,
            'wid':i.WORKER.id
        })
    return JsonResponse({'status': 'ok', 'data': l})


def w_delete_service(request):
    sid=request.POST['sid']
    Worker_Service.objects.filter(id=sid).delete()
    return JsonResponse({'status': 'ok'})



def worker_view_service_request(request):
    lid=request.POST['lid']
    re=Worker_Request.objects.filter(WORKER_SERVICE__WORKER__LOGIN_id=lid,status='pending').order_by('-date')
    l=[]
    for i in re:
        lat = Location.objects.get(LOGIN_id=i.USER.LOGIN.id).latitude
        longi = Location.objects.get(LOGIN_id=i.USER.LOGIN.id).longitude

        l.append({
            'id':i.id,
            'date':i.date,
            'status':i.status,
            'sname':i.WORKER_SERVICE.name,
            'charge':i.WORKER_SERVICE.charge,
            'name': i.USER.uname,
            'phone': i.USER.phone,
            # 'photo': i.WORKER_SERVICE.WORKER.photo,
            'email': i.USER.email,
            'place': i.USER.place,
            'wid': i.USER.LOGIN.id,
            'lat': lat,
            'longi': longi
        })
    return JsonResponse({'status':'ok','data':l})

def worker_view_approved_service_request(request):
    lid=request.POST['lid']
    re = Worker_Request.objects.filter(
        Q(WORKER_SERVICE__WORKER__LOGIN_id=lid) & (Q(status='Approved') | Q(status='Paid'))
    ).order_by('-date')
    # re = Worker_Request.objects.filter(
    #     WORKER_SERVICE__WORKER__LOGIN_id=lid,
    #     Q(status='Approved') | Q(status='Paid')
    # ).order_by('-date')
    # re=Worker_Request.objects.filter(WORKER_SERVICE__WORKER__LOGIN_id=lid,status='Approved').order_by('-date')
    l=[]
    for i in re:
        lat = Location.objects.get(LOGIN_id=i.USER.LOGIN.id).latitude
        longi = Location.objects.get(LOGIN_id=i.USER.LOGIN.id).longitude

        l.append({
            'id':i.id,
            'date':i.date,
            'status':i.status,
            'sname':i.WORKER_SERVICE.name,
            'charge':i.WORKER_SERVICE.charge,
            'name': i.USER.uname,
            'phone': i.USER.phone,
            # 'photo': i.WORKER_SERVICE.WORKER.photo,
            'email': i.USER.email,
            'place': i.USER.place,
            'wid': i.USER.LOGIN.id,
            'lat': lat,
            'longi': longi
        })
    return JsonResponse({'status':'ok','data':l})


def worker_view_rejected_service_request(request):
    lid=request.POST['lid']
    # re = Worker_Request.objects.filter(
    #     Q(WORKER_SERVICE__WORKER__LOGIN_id=lid) & (Q(status='Approved') | Q(status='Paid'))
    # ).order_by('-date')
    # re = Worker_Request.objects.filter(
    #     WORKER_SERVICE__WORKER__LOGIN_id=lid,
    #     Q(status='Approved') | Q(status='Paid')
    # ).order_by('-date')
    re=Worker_Request.objects.filter(WORKER_SERVICE__WORKER__LOGIN_id=lid,status='Rejected').order_by('-date')
    l=[]
    for i in re:
        lat = Location.objects.get(LOGIN_id=i.USER.LOGIN.id).latitude
        longi = Location.objects.get(LOGIN_id=i.USER.LOGIN.id).longitude

        l.append({
            'id':i.id,
            'date':i.date,
            'status':i.status,
            'sname':i.WORKER_SERVICE.name,
            'charge':i.WORKER_SERVICE.charge,
            'name': i.USER.uname,
            'phone': i.USER.phone,
            # 'photo': i.WORKER_SERVICE.WORKER.photo,
            'email': i.USER.email,
            'place': i.USER.place,
            'wid': i.USER.LOGIN.id,
            'lat': lat,
            'longi': longi
        })
    return JsonResponse({'status':'ok','data':l})



def worker_approve_request(request):
    id=request.POST['id']
    Worker_Request.objects.filter(id=id).update(status='Approved')
    return JsonResponse({'status':'ok'})


def worker_reject_request(request):
    id=request.POST['id']
    Worker_Request.objects.filter(id=id).update(status='Rejected')
    return JsonResponse({'status':'ok'})


#=====Chat with user============

def worker_sendchat(request):
    FROM_id=request.POST['from_id']
    TOID_id=request.POST['to_id']
    #print(FROM_id)
    #print(TOID_id)
    msg=request.POST['message']

    from  datetime import datetime
    c=Chat()
    c.FROMID_id=FROM_id
    c.TOID_id=TOID_id
    c.message=msg
    c.date=datetime.now()
    c.save()
    return JsonResponse({'status':"ok"})


def worker_viewchat(request):
    fromid = request.POST["from_id"]
    toid = request.POST["to_id"]
    # lmid = request.POST["lastmsgid"]
    from django.db.models import Q

    res = Chat.objects.filter(Q(FROMID_id=fromid, TOID_id=toid) | Q(FROMID_id=toid, TOID_id=fromid))
    l = []

    for i in res:
        l.append({"id": i.id, "msg": i.message, "from": i.FROMID_id, "date": i.date, "to": i.TOID_id})

    return JsonResponse({"status":"ok",'data':l})



def worker_view_service_review(request):
    sid=request.POST['sid']
    print(sid)
    obj = Service_Review.objects.filter(WORKERSERVICE_id=sid)
    l = []
    for i in obj:
        l.append({'id': i.id, 'review': i.review,
                  'date': i.date, 'email': i.USER.email,
                  'user': i.USER.uname})
    print(l)
    return JsonResponse({'status': 'ok', 'data': l})





def worker_change_password(request):
    lid = request.POST['lid']
    oldp = request.POST['old']
    newp = request.POST['new']
    conp = request.POST['confirm']
    log = Login.objects.filter(id=lid, password=oldp)
    if log.exists():
        log = Login.objects.filter(id=lid, password=oldp).update(password=newp)
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'no'})


def w_view_payment(request):
    lid=request.POST['lid']
    re=Service_Payment.objects.filter(WORKER_REQUEST__WORKER_SERVICE__WORKER__LOGIN_id=lid).order_by('-date')
    l=[]
    for i in re:
        l.append({
            'id':i.id,
            'date':i.date,
            'uname':i.WORKER_REQUEST.USER.uname,
            'sname':i.WORKER_REQUEST.WORKER_SERVICE.name,
            'charge':i.WORKER_REQUEST.WORKER_SERVICE.charge
        })
    return JsonResponse({'status': 'ok', 'data': l})



#====================User========================================

def user_signup_post(request):
    name=request.POST['name']
    email=request.POST['email']
    phone=request.POST['phone']
    place=request.POST['place']
    pin=request.POST['pin']
    district=request.POST['district']
    state=request.POST['state']
    # from datetime import datetime
    # date=datetime.now().strftime("%Y%m%d-%H%M%S")+".jpg"
    photo=request.POST['photo']

    import datetime
    import base64
    #
    date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    a = base64.b64decode(photo)
    fh = open("C:\\Users\\asus\\PycharmProjects\\road sense\\road_sense\\media\\user\\" + date + ".jpg", "wb")
    # fh = open("C:\\Users\\91815\\PycharmProjects\\cyber\\media\\" + date + ".jpg", "wb")
    path = "/media/user/" + date + ".jpg"
    fh.write(a)
    fh.close()
    password = request.POST['password']
    cpassword = request.POST['cpassword']

    ss=Users.objects.filter(email=email)
    if ss.exists():
        return JsonResponse({'status': 'no'})

    lobj = Login()
    lobj.username = email
    lobj.password = cpassword
    lobj.type = 'user'
    lobj.save()

    uobj = Users()
    uobj.uname = name
    uobj.phone = phone
    uobj.email = email
    uobj.photo = path
    uobj.place = place
    uobj.pincode = pin
    uobj.district = district
    uobj.state = state
    uobj.LOGIN = lobj
    uobj.save()
    return JsonResponse({'status': 'ok'})


def user_view_profile(request):
    lid = request.POST['lid']
    res = Users.objects.get(LOGIN=lid)
    #print(res)
    return JsonResponse({'status': 'ok', 'name': res.uname, 'email': res.email, 'phone': res.phone,
                          'photo': res.photo,'place': res.place,
                         'pin': res.pincode, 'district': res.district,'state':res.state})

def user_edit_profile(request):
    lid=request.POST['lid']
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    place = request.POST['place']
    pin = request.POST['pin']
    district = request.POST['district']
    state = request.POST['state']
    photo = request.POST['photo']
    uobj = Users.objects.get(LOGIN=lid)
    uobj.name = name
    uobj.phone = phone
    uobj.email = email
    if len(photo)>0:
        import datetime
        import base64
        #
        date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        a = base64.b64decode(photo)
        fh = open("C:\\road_sense\\media\\user\\" + date + ".jpg", "wb")
        # fh = open("C:\\Users\\91815\\PycharmProjects\\cyber\\media\\" + date + ".jpg", "wb")
        path = "/media/user/" + date + ".jpg"
        fh.write(a)
        fh.close()
        uobj.photo = path
    uobj.place = place
    uobj.pincode = pin
    uobj.district = district
    uobj.state = state
    uobj.save()
    return JsonResponse({'status': 'ok'})



def user_view_evstation(request):
    se=request.POST['se']
    re=Evstation.objects.filter(status='Approved',place__icontains=se)
    l=[]
    for i in re:
        l.append({
            'id':i.id,
            'stationname':i.stationname,
            'place':i.place,
            'phone':i.phone,
            'email':i.email,
            'district':i.district,
            'state':i.state,
            'logid':i.LOGIN.id


        })
    return JsonResponse({'status':'ok','data':l})

def get_nearest_ev(request):
    se=request.POST['se']

    from django.db.models import FloatField, F, Value, Q
    from django.db.models.functions import Sqrt, Sin, Cos, Radians, ACos, Cast
    current_latitude = request.POST['lat']
    current_longitude = request.POST['lon']

    EARTH_RADIUS = 6371

    hospitals = Evstation.objects.annotate(
        # Convert CharField latitude and longitude to FloatField
        lati=Cast('latitude', FloatField()),
        lon=Cast('longitude', FloatField())
    ).annotate(
        distance=EARTH_RADIUS * ACos(
            Cos(Radians(Value(current_latitude))) * Cos(Radians(F('lati'))) *
            Cos(Radians(F('lon')) - Radians(Value(current_longitude))) +
            Sin(Radians(Value(current_latitude))) * Sin(Radians(F('lati')))
        )
    ).filter(
        distance__lte=10,place__icontains=se,status='Approved'
    ).order_by('distance')

    l = []
    for i in hospitals:
        l.append({
            'id': i.id,
            'stationname': i.stationname,
            'place': i.place,
            'phone': i.phone,
            'email': i.email,
            'district': i.district,
            'state': i.state,
            'logid': i.LOGIN.id

        })
    return JsonResponse({'status': 'ok', 'data': l})





def user_view_charging_point(request):
    ev=request.POST['evid']
    re=Charging_point.objects.filter(EV_id=ev)
    l=[]
    for i in re:
        l.append({
            'id':i.id,
            'speed':i.speed,
            'outlettype':i.outlettype,
            'number_of_outlets':i.number_of_outlets,
            'Price':i.Price,
            'EV':i.EV.id,

        })
    return JsonResponse({'status':'ok','data':l})

def user_view_charging_slot(request):
    cp=request.POST['cid']
    from datetime import datetime
    date=datetime.now().today()
    re=Slots.objects.filter(CHARGINGPOINT_id=cp,date__gte=date).order_by('-date')
    l=[]

    for i in re:
        r=Slots.objects.get(id=i.id).slots

        if r>=1:
            l.append({
                'id':i.id,
                'date':i.date,
                'slots':i.slots,
                'cp':i.CHARGINGPOINT.id
            })
            return JsonResponse({'status':'ok','data':l})
    else:
        return JsonResponse({'status': 'no', 'data': l})


def user_book_ev_slot(request):
    slot=request.POST['sid']
    lid=request.POST['lid']
    ss=Slotbooking()
    ss.SLOTS=Slots.objects.get(id=slot)
    from datetime import datetime
    date=datetime.now().today()
    ss.USER=Users.objects.get(LOGIN_id=lid)
    ss.date=date
    ss.status='pending'
    ss.save()

    Slots.objects.filter(id=slot).update(slots=F('slots') - 1)

    # Slots.objects.filter(id=slot).update(slots=(solts-1))

    pp=Payment()
    pp.SLOTBOOKING=Slotbooking.objects.get(id=ss.id)
    pp.date=date
    pp.status='paid'
    pp.save()

    Slotbooking.objects.filter(id=ss.id).update(status='paid')
    return JsonResponse({'status': 'ok'})


def user_view_ev_bookings(request):
    lid=request.POST['lid']
    ss=Slotbooking.objects.filter(USER__LOGIN_id=lid).order_by('-date')
    l=[]
    for i in ss:
        l.append({
            'id':i.id,
            'ctype':i.SLOTS.CHARGINGPOINT.outlettype,
            'cspeed':i.SLOTS.CHARGINGPOINT.speed,
            'cprice':i.SLOTS.CHARGINGPOINT.Price,
            'date':i.date,
            'evname':i.SLOTS.CHARGINGPOINT.EV.stationname,
            'place':i.SLOTS.CHARGINGPOINT.EV.place,
            'phone':i.SLOTS.CHARGINGPOINT.EV.phone,
            'evid':i.SLOTS.CHARGINGPOINT.EV.id

        })
    return JsonResponse({'status': 'ok', 'data': l})


def user_send_ev_review(request):
    lid=request.POST['lid']
    evid=request.POST['evid']
    review=request.POST['review']
    from datetime import datetime
    date=datetime.now().today()
    cc=Users.objects.get(LOGIN=lid)
    cobj=Ev_Review()
    cobj.USER=cc
    cobj.EV=Evstation.objects.get(id=evid)
    cobj.review=review
    cobj.date=date
    cobj.save()

    analyzer = SentimentIntensityAnalyzer()
    # for sentence in review:
    vs = analyzer.polarity_scores(review)
    #print("{:-<65} {}".format(review, str(vs)))

    if vs['neg'] > 0:
        # rr=Worker_Service.objects.get(id=ws).negative

        Evstation.objects.filter(id=evid).update(negative=models.F('negative') + vs['neg'])

    elif vs['pos'] > 0:
        # rr=Worker_Service.objects.get(id=ws).positive
        Evstation.objects.filter(id=evid).update(positive=models.F('positive') + vs['pos'])
    else:
        Evstation.objects.filter(id=evid).update(neutral=models.F('neutral') + vs['neu'])

    return JsonResponse({'status':'ok'})


def user_view_ev_review(request):
    eid=request.POST['evid']
    # cc=Users.objects.get(LOGIN=lid)
    obj=Ev_Review.objects.filter(EV_id=eid).order_by('EV__positive')
    l=[]
    for i in obj:
        l.append({'id':i.id,'review':i.review,'date':i.date,'email':i.USER.email,'user':i.USER.uname})
    return JsonResponse({'status':'ok','data':l})


def user_view_fuelstation(request):
    # re=Fuelstation.objects.filter(status='Approved',)
    from datetime import datetime
    date=datetime.now().today()
    re=Work_status.objects.filter(status='active',FUEL__status='Approved',date=date)
    l = []
    for i in re:
        l.append({
            'id': i.FUEL.id,
            'stationname': i.FUEL.stationname,
            'place': i.FUEL.place,
            'phone': i.FUEL.phone,
            'email': i.FUEL.email,
            'district': i.FUEL.district,
            'state': i.FUEL.state,
            'logid': i.FUEL.LOGIN.id,


        })
    return JsonResponse({'status': 'ok', 'data': l})


def get_nearest_fs(request):
    se=request.POST['se']

    from django.db.models import FloatField, F, Value, Q
    from django.db.models.functions import Sqrt, Sin, Cos, Radians, ACos, Cast
    current_latitude = request.POST['lat']
    current_longitude = request.POST['lon']

    EARTH_RADIUS = 6371

    hospitals = Fuelstation.objects.annotate(
        # Convert CharField latitude and longitude to FloatField
        lati=Cast('latitude', FloatField()),
        lon=Cast('longitude', FloatField())
    ).annotate(
        distance=EARTH_RADIUS * ACos(
            Cos(Radians(Value(current_latitude))) * Cos(Radians(F('lati'))) *
            Cos(Radians(F('lon')) - Radians(Value(current_longitude))) +
            Sin(Radians(Value(current_latitude))) * Sin(Radians(F('lati')))
        )
    ).filter(
        distance__lte=10,place__icontains=se,status='Approved'
    ).order_by('distance')

    l = []
    for i in hospitals:
        l.append({
            'id': i.id,
            'stationname': i.stationname,
            'place': i.place,
            'phone': i.phone,
            'email': i.email,
            'district': i.district,
            'state': i.state,
            'logid': i.LOGIN.id

        })
    return JsonResponse({'status': 'ok', 'data': l})



def user_view_fuelstock(request):
    fid=request.POST['fid']
    re=Fuel_Stock.objects.filter(FUEL_id=fid)
    l=[]
    for i in re:
        # ree=Fuel_Stock.objects.filter(FUEL_id=fid).stock
        if int(i.stock) >= 1:
            l.append({
                'id':i.id,
                'f_id':i.FUEL.id,
                'fuel':i.fuel_type,
                'brand':i.brand,
                'quantity':i.quantity,
                'price':i.price,
                'stock':i.stock
            })
    return JsonResponse({'status': 'ok', 'data': l})

def user_book_fuel(request):
    lid=request.POST['lid']
    fid=request.POST['fid']
    ff=Fuel_Booking()
    ff.FUEL_STOCK=Fuel_Stock.objects.get(id=fid)
    from datetime import datetime
    date = datetime.now().today()
    ff.date=date
    ff.USER=Users.objects.get(LOGIN_id=lid)
    ff.save()

    Fuel_Stock.objects.filter(id=fid).update(stock=F('stock') - 1)


    fs=Fuel_Payment()
    fs.FUELBOOKING_id=ff.id
    fs.date=date
    fs.status='paid'
    fs.save()
    return JsonResponse({'status': 'ok'})


def user_view_fuel_booking(request):
    lid=request.POST['lid']
    re=Fuel_Booking.objects.filter(USER__LOGIN_id=lid)
    l=[]
    for i in re:
        l.append({
            'id':i.id,
            'date':i.date,
            'fname':i.FUEL_STOCK.fuel_type,
            'fbrand':i.FUEL_STOCK.brand,
            'quantity':i.FUEL_STOCK.quantity,
            'price':i.FUEL_STOCK.price,
            'fstation':i.FUEL_STOCK.FUEL.stationname,
            'place':i.FUEL_STOCK.FUEL.place,
            'fsphone':i.FUEL_STOCK.FUEL.phone,
            'fsid':i.FUEL_STOCK.FUEL.id

        })

    return JsonResponse({'status': 'ok', 'data': l})


def user_send_fs_review(request):
    lid=request.POST['lid']
    fsid=request.POST['fsid']
    review=request.POST['review']
    from datetime import datetime
    date=datetime.now().today()
    cc=Users.objects.get(LOGIN=lid)
    cobj=Fs_Review()
    cobj.USER=cc
    cobj.FS=Fuelstation.objects.get(id=fsid)
    cobj.review=review
    cobj.date=date
    cobj.save()
    analyzer = SentimentIntensityAnalyzer()
    # for sentence in review:
    vs = analyzer.polarity_scores(review)
    #print("{:-<65} {}".format(review, str(vs)))

    if vs['neg'] > 0:
        # rr=Worker_Service.objects.get(id=ws).negative

        Fuelstation.objects.filter(id=fsid).update(negative=models.F('negative') + vs['neg'])

    elif vs['pos'] > 0:
        # rr=Worker_Service.objects.get(id=ws).positive
        Fuelstation.objects.filter(id=fsid).update(positive=models.F('positive') + vs['pos'])
    else:
        Fuelstation.objects.filter(id=fsid).update(neutral=models.F('neutral') + vs['neu'])


    return JsonResponse({'status':'ok'})



def user_view_fs_review(request):
    eid=request.POST['fsid']
    # cc=Users.objects.get(LOGIN=lid)
    obj=Fs_Review.objects.filter(FS_id=eid).order_by('positive')
    l=[]
    for i in obj:
        l.append({'id':i.id,'review':i.review,'date':i.date,'email':i.USER.email,'user':i.USER.uname})
    return JsonResponse({'status':'ok','data':l})







def _update_location(request):
    lid=request.POST['lid']
    lat=request.POST['lat']
    lon=request.POST['lon']
    dobj=Location()
    if Location.objects.filter(LOGIN_id=lid).exists():
        dobj = Location.objects.get(LOGIN_id=lid)
    dobj.latitude=lat
    dobj.longitude=lon
    dobj.LOGIN_id=lid
    dobj.save()
    return JsonResponse({'status':'ok'})

def user_send_complaint(request):
    lid=request.POST['lid']
    complaaint=request.POST['complaint']
    from datetime import datetime
    date=datetime.now().strftime("%Y-%m-%d")
    cc=Users.objects.get(LOGIN=lid)
    cobj=Complaints()
    cobj.USER=cc
    cobj.complaint=complaaint
    cobj.date=date
    cobj.status='pending'
    cobj.reply='pending'
    cobj.save()
    return JsonResponse({'status':'ok'})

def user_view_complaint_post(request):
    lid=request.POST['lid']
    cc=Users.objects.get(LOGIN=lid)
    obj=Complaints.objects.filter(USER=cc)
    l=[]
    for i in obj:
        l.append({'id':i.id,'comp':i.complaint,'date':i.date,'status':i.status,'reply':i.reply})
    return JsonResponse({'status':'ok','data':l})

def user_appreview_post(request):
    lid=request.POST['lid']
    cc=Users.objects.get(LOGIN=lid)
    feedback=request.POST['review']
    rating=request.POST['rating']
    from datetime import datetime
    date = datetime.now().strftime("%Y-%m-%d")
    fobj=Review_app()
    fobj.USER=cc
    fobj.review=feedback
    fobj.rating=rating
    fobj.date=date
    fobj.save()
    return JsonResponse({'status':'ok'})

def user_view_appreview_post(request):
    lid=request.POST['lid']
    cc = Users.objects.get(LOGIN=lid)
    res=Review_app.objects.filter(USER=cc)
    l=[]
    for i in res:
        l.append({'id':i.id,'feedback':i.review,'date':i.date,'rating':i.rating})
    return JsonResponse({'status':'ok','data':l})

def user_view_service(request):
    se=request.POST['se']
    lat_u=request.POST['lat']
    lon_u=request.POST['lon']
    # #print(request.POST,"abcd")
    re=Worker_Service.objects.filter(name__icontains=se)

    l=[]

    for i in re:
        ll=Location.objects.filter(LOGIN_id=i.WORKER.LOGIN.id)
        if ll.exists():

            lat=Location.objects.get(LOGIN_id=i.WORKER.LOGIN.id).latitude
            longi=Location.objects.get(LOGIN_id=i.WORKER.LOGIN.id).longitude

            # loc1 = (19.0760, 72.8777)  # Mumbai
            loc1 = (float(lat_u), float(lon_u))  # Mumbai
            # loc2 = (18.5204, 73.8567)  # Pune
            loc2 = (float(lat), float(longi))

            # #print(loc1,loc2)# Pune

            distance = haversine(loc1, loc2, unit=Unit.KILOMETERS)
            # #print(distance,"")

            l.append({
                'id':i.id,
                'wid':i.WORKER.id,
                'wname':i.WORKER.wname,
                'charge':i.charge,
                'name':i.name,
                'phone':i.WORKER.phone,
                'photo':i.WORKER.photo,
                'email':i.WORKER.email,
                'place':i.WORKER.place,
                'lat':lat,
                'longi':longi,
                'distance':distance


            })

            for i in range(0,len(l)):
                for j in range(0,len(l)):
                    # dist=i.distance
                    #print(l[i]['distance'],"abcdef")
                    #print(l[j]['distance'],"xyz")

                    if float(l[i]['distance']) < float(l[j]['distance']) :
                        temp=l[i]
                        l[i]=l[j]
                        # samp=l[j].distance
                        l[j]=temp

        #print(l)

    return JsonResponse({'status':'ok','data':l})



def u_send_service_request(request):
    id=request.POST['sid']
    lid=request.POST['lid']
    wr=Worker_Request()
    wr.WORKER_SERVICE=Worker_Service.objects.get(id=id)
    from datetime import datetime
    wr.date=datetime.now().today()
    wr.USER=Users.objects.get(LOGIN_id=lid)
    wr.status='pending'
    wr.save()
    return JsonResponse({'status':'ok'})

def user_view_service_request(request):
    lid=request.POST['lid']
    re=Worker_Request.objects.filter(USER__LOGIN_id=lid)
    l=[]
    for i in re:
        lat = Location.objects.get(LOGIN_id=i.WORKER_SERVICE.WORKER.LOGIN.id).latitude
        longi = Location.objects.get(LOGIN_id=i.WORKER_SERVICE.WORKER.LOGIN.id).longitude

        l.append({
            'id':i.id,
            'date':i.date,
            'status':i.status,
            'sname':i.WORKER_SERVICE.name,
            'charge':i.WORKER_SERVICE.charge,
            'wname': i.WORKER_SERVICE.WORKER.wname,
            'phone': i.WORKER_SERVICE.WORKER.phone,
            'photo': i.WORKER_SERVICE.WORKER.photo,
            'email': i.WORKER_SERVICE.WORKER.email,
            'place': i.WORKER_SERVICE.WORKER.place,
            'wid': i.WORKER_SERVICE.WORKER.LOGIN.id,
            'lat': lat,
            'longi': longi
        })
    return JsonResponse({'status':'ok','data':l})


def user_service_payment(request):
    # lid=request.POST['lid']
    sid=request.POST['sid']
    from datetime import datetime
    date=datetime.now().today()

    fs=Service_Payment()
    fs.WORKER_REQUEST_id=sid
    fs.date=date
    fs.status='paid'
    fs.save()

    Worker_Request.objects.filter(id=sid).update(status='Paid')
    return JsonResponse({'status': 'ok'})


def user_send_service_review(request):
    lid=request.POST['lid']
    sid=request.POST['sid']
    ws=Worker_Request.objects.get(id=sid).WORKER_SERVICE.id
    print(ws,"wwwwwwwwwwww")
    review=request.POST['review']
    from datetime import datetime
    date=datetime.now().today()
    cc=Users.objects.get(LOGIN=lid)
    cobj=Service_Review()
    cobj.USER=cc
    cobj.WORKERSERVICE=Worker_Service.objects.get(id=ws)
    cobj.review=review
    cobj.date=date
    cobj.save()

    # sentences = ["VADER is smart, handsome, and funny.",  # positive sentence example
    #              "VADER is not smart, handsome, nor funny.",  # negation sentence example
    #              "VADER is smart, handsome, and funny!",
    #              # punctuation emphasis handled correctly (sentiment intensity adjusted)
    #              "VADER is very smart, handsome, and funny.",
    #              # booster words handled correctly (sentiment intensity adjusted)
    #              "VADER is VERY SMART, handsome, and FUNNY.",  # emphasis for ALLCAPS handled
    #              "VADER is VERY SMART, handsome, and FUNNY!!!",
    #              # combination of signals - VADER appropriately adjusts intensity
    #              "VADER is VERY SMART, uber handsome, and FRIGGIN FUNNY!!!",
    #              # booster words & punctuation make this close to ceiling for score
    #              "The book was good.",  # positive sentence
    #              "The book was kind of good.",  # qualified positive sentence is handled correctly (intensity adjusted)
    #              "The plot was good, but the characters are uncompelling and the dialog is not great.",
    #              # mixed negation sentence
    #              "At least it isn't a horrible book.",  # negated negative sentence with contraction
    #              "Make sure you :) or :D today!",  # emoticons handled
    #              "Today SUX!",  # negative slang with capitalization emphasis
    #              "Today only kinda sux! But I'll get by, lol"
    #              # mixed sentiment example with slang and constrastive conjunction "but"
    #              ]
    #
    analyzer = SentimentIntensityAnalyzer()
    # for sentence in review:
    vs = analyzer.polarity_scores(review)
    #print("{:-<65} {}".format(review, str(vs)))


    if vs['neg']>0:
        # rr=Worker_Service.objects.get(id=ws).negative

        Worker_Service.objects.filter(id=ws).update(negative=models.F('negative') + vs['neg'])

    elif vs['pos']>0:
        # rr=Worker_Service.objects.get(id=ws).positive
        Worker_Service.objects.filter(id=ws).update(positive=models.F('positive') + vs['pos'])
    else:
        Worker_Service.objects.filter(id=ws).update(neutral=models.F('neutral') + vs['neu'])





    return JsonResponse({'status':'ok'})


def user_view_service_review(request):
    sid=request.POST['sid']
    obj = Service_Review.objects.filter(WORKERSERVICE_id=sid)
    l = []
    for i in obj:
        l.append({'id': i.id, 'review': i.review,
                  'date': i.date, 'email': i.USER.email,
                  'user': i.USER.uname})
    return JsonResponse({'status': 'ok', 'data': l})





#===========Chat with worker=======================

def User_sendchat(request):
    FROM_id=request.POST['from_id']
    TOID_id=request.POST['to_id']
    #print(FROM_id)
    #print(TOID_id)
    msg=request.POST['message']

    from  datetime import datetime
    c=Chat()
    c.FROMID_id=FROM_id
    c.TOID_id=TOID_id
    c.message=msg
    c.date=datetime.now()
    c.save()
    return JsonResponse({'status':"ok"})


def User_viewchat(request):
    fromid = request.POST["from_id"]
    toid = request.POST["to_id"]
    # lmid = request.POST["lastmsgid"]
    from django.db.models import Q

    res = Chat.objects.filter(Q(FROMID_id=fromid, TOID_id=toid) | Q(FROMID_id=toid, TOID_id=fromid))
    l = []

    for i in res:
        l.append({"id": i.id, "msg": i.message, "from": i.FROMID_id, "date": i.date, "to": i.TOID_id})

    return JsonResponse({"status":"ok",'data':l})

