from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model

class CustomUser(AbstractUser):
    is_customer = models.BooleanField()
    is_Technician = models.BooleanField()
    phoneNumber = models.IntegerField()  
    # img = models.ImageField(upload_to='images/', height_field=None, width_field=None, max_length=None)

class Customer(models.Model):
    User = models.ForeignKey(
        CustomUser, 
        verbose_name=("Customer's User"), 
        on_delete=models.CASCADE)
    address = models.CharField(max_length=50)

class Device(models.Model):
    devicename = models.CharField(max_length=50)
    deviceDescription = models.CharField(max_length=50)
    
    def __str__(self):
        return self.devicename
    
class Technician(models.Model):
    user = models.ForeignKey(
        CustomUser, 
        verbose_name=("Technicians's User"), 
        on_delete=models.CASCADE)
    organizationName = models.CharField(max_length=50)
    ProfilePicture = models.ImageField(
                            upload_to='images/', 
                            height_field=None, 
                            width_field=None, 
                            max_length=None)
    Location = models.CharField(max_length=50)
    isApproved = models.BooleanField(default= False)
    rating = models.IntegerField(default = 0)
    device = models.ForeignKey(
        Device, 
        verbose_name= (""), 
        on_delete=models.CASCADE,
        related_name= 'technicianDevice')
    


class Admin(models.Model):
    User = models.ForeignKey(
        CustomUser, 
        verbose_name=("admin's User"), 
        on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique = True)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique = True)

class Order(models.Model):
    User = models.ForeignKey(
        CustomUser, 
        verbose_name=("customer"), 
        on_delete=models.CASCADE,
        null = True)
    technician = models.ForeignKey(
        Technician, 
        verbose_name=("technician"), 
        related_name= 'ordertechnician',
        on_delete=models.CASCADE,
        null = True)
    device = models.ForeignKey(
        Device, 
        verbose_name=("Order Device"), 
        on_delete=models.CASCADE,
        related_name= 'orderDevice',
        null=False)
    status = models.BooleanField(default=False)
    date = models.DateField(auto_now=True) #, auto_now_add=True)
    
    def updateStatus(self):
        self.status = True
    
    
class Payment(models.Model):
    payer = models.ForeignKey(
        CustomUser, 
        verbose_name=("payer"), 
        on_delete=models.CASCADE)
    order = models.ForeignKey(
        CustomUser, 
        verbose_name=("payer"), 
        on_delete=models.CASCADE,
        related_name= 'paymentOrder')
    PaymentType = models.CharField(max_length=50)
    price = models.IntegerField()
    status = models.BooleanField()
    accountInformation = models.CharField(max_length=50)

class Feedback(models.Model):
    user = models.ForeignKey(
        CustomUser, 
        verbose_name=("Feedback Giver"), 
        on_delete=models.CASCADE,
        null=True, blank= True)
    subject = models.CharField(max_length=50)
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)

class test(models.Model):
    username = models.CharField( max_length=50)
    name = models.CharField(max_length=50)

class image(models.Model):
    myimage = models.ImageField(upload_to="images")