from django.db import models

# Create your models here.
class Login(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    type=models.CharField(max_length=30)

class Evstation(models.Model):
    stationname=models.CharField(max_length=300)
    place=models.CharField(max_length=300)
    licenseno=models.CharField(max_length=500)
    phone=models.CharField(max_length=10)
    email=models.CharField(max_length=50)
    pincode=models.CharField(max_length=50)
    district=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    latitude=models.CharField(max_length=50,default="")
    longitude=models.CharField(max_length=50,default="")
    positive = models.CharField(max_length=100, default='')
    negative = models.CharField(max_length=100, default='')
    neutral = models.CharField(max_length=100, default='')
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)

class Fuelstation(models.Model):
    stationname=models.CharField(max_length=300)
    place=models.CharField(max_length=300)
    licenseno=models.CharField(max_length=500)
    phone=models.CharField(max_length=10)
    email=models.CharField(max_length=50)
    pincode=models.CharField(max_length=50)
    district=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    latitude = models.CharField(max_length=50, default="")
    longitude = models.CharField(max_length=50, default="")
    positive = models.BigIntegerField(default=0)
    negative = models.BigIntegerField(default=0)
    neutral = models.BigIntegerField(default=0)
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)

class Workers(models.Model):
    wname=models.CharField(max_length=300)
    place=models.CharField(max_length=300)
    gender=models.CharField(max_length=50)
    dob=models.CharField(max_length=50)
    phone=models.CharField(max_length=10)
    email=models.CharField(max_length=50)
    experience=models.CharField(max_length=50)
    qualification=models.CharField(max_length=50)
    certificate=models.CharField(max_length=500)
    photo=models.CharField(max_length=500)
    district=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
class Users(models.Model):
    uname=models.CharField(max_length=30)
    place=models.CharField(max_length=300)
    pincode=models.CharField(max_length=50)
    phone=models.CharField(max_length=10)
    email=models.CharField(max_length=50)
    photo=models.CharField(max_length=500)
    district=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)

class Complaints(models.Model):
    complaint=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    reply=models.CharField(max_length=50)
    date=models.CharField(max_length=50)
    USER=models.ForeignKey(Users,on_delete=models.CASCADE,default=1)

class Review_app(models.Model):
    date = models.DateField()
    USER=models.ForeignKey(Users,on_delete=models.CASCADE)
    review=models.CharField(max_length=100)
    rating=models.CharField(max_length=100)


class Ev_Review(models.Model):
    date = models.DateField()
    USER=models.ForeignKey(Users,on_delete=models.CASCADE)
    EV=models.ForeignKey(Evstation,on_delete=models.CASCADE)
    review=models.CharField(max_length=100)


    # rating=models.CharField(max_length=100)

class Charging_point(models.Model):
    speed=models.CharField(max_length=100)
    outlettype=models.CharField(max_length=100)
    number_of_outlets=models.CharField(max_length=100)
    Price=models.CharField(max_length=100)
    EV=models.ForeignKey(Evstation,on_delete=models.CASCADE)

class Slots(models.Model):
    CHARGINGPOINT=models.ForeignKey(Charging_point,on_delete=models.CASCADE,default=1)
    date=models.DateField(default="")
    slots=models.BigIntegerField(default=1)
class Slotbooking(models.Model):
    SLOTS=models.ForeignKey(Slots,on_delete=models.CASCADE,default="")
    USER=models.ForeignKey(Users,on_delete=models.CASCADE,default="")
    status=models.CharField(max_length=30)
    date=models.DateField(default="2024-06-10")

class Payment(models.Model):
    SLOTBOOKING=models.ForeignKey(Slotbooking,on_delete=models.CASCADE,default="")
    date=models.DateField()
    status=models.CharField(max_length=30,default="")





class Location(models.Model):
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    latitude=models.CharField(max_length=100)
    longitude=models.CharField(max_length=100)


class Service(models.Model):
    name=models.CharField(max_length=300)
    charge=models.BigIntegerField()
    WORKER=models.ForeignKey(Workers,on_delete=models.CASCADE,default="")



class Work_status(models.Model):
    status=models.CharField(max_length=300)
    date=models.DateField()
    FUEL=models.ForeignKey(Fuelstation,on_delete=models.CASCADE,default="")


class Fuel_Stock(models.Model):
    FUEL=models.ForeignKey(Fuelstation,on_delete=models.CASCADE,default="")
    fuel_type=models.CharField(max_length=300)
    brand=models.CharField(max_length=300)
    quantity=models.CharField(max_length=300)
    price=models.CharField(max_length=300)
    stock=models.CharField(max_length=300)

class Fuel_Booking(models.Model):
    FUEL_STOCK=models.ForeignKey(Fuel_Stock,on_delete=models.CASCADE)
    date=models.DateField()
    USER=models.ForeignKey(Users,on_delete=models.CASCADE,default="")

class Fuel_Payment(models.Model):
    FUELBOOKING=models.ForeignKey(Fuel_Booking,on_delete=models.CASCADE,default="")
    date=models.DateField()
    status=models.CharField(max_length=30,default="")

class Fs_Review(models.Model):
    date = models.DateField()
    USER=models.ForeignKey(Users,on_delete=models.CASCADE)
    FS=models.ForeignKey(Fuelstation,on_delete=models.CASCADE)
    review=models.CharField(max_length=100)


class Worker_Service(models.Model):
    WORKER=models.ForeignKey(Workers,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    charge=models.CharField(max_length=100)
    positive = models.BigIntegerField(default=0)
    negative = models.BigIntegerField(default=0)
    neutral = models.BigIntegerField(default=0)

class Worker_Request(models.Model):
    WORKER_SERVICE=models.ForeignKey(Worker_Service,on_delete=models.CASCADE)
    date = models.DateField()
    USER=models.ForeignKey(Users,on_delete=models.CASCADE)
    status=models.CharField(max_length=30,default="")


class Chat(models.Model):
    FROMID=models.ForeignKey(Login,on_delete=models.CASCADE,related_name="fromc")
    TOID=models.ForeignKey(Login,on_delete=models.CASCADE,related_name="toc")
    message=models.CharField(max_length=600)
    date = models.DateField()

class Service_Payment(models.Model):
    WORKER_REQUEST=models.ForeignKey(Worker_Request,on_delete=models.CASCADE,default="")
    date=models.DateField()
    status=models.CharField(max_length=30,default="")

class Service_Review(models.Model):
    date = models.DateField()
    USER=models.ForeignKey(Users,on_delete=models.CASCADE)
    WORKERSERVICE=models.ForeignKey(Worker_Service,on_delete=models.CASCADE)
    review=models.CharField(max_length=100)












