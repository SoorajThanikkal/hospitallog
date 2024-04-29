# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class reg(models.Model):
    STATUS_CHOICE=(
        ('pending','PENDING'),
        ('approved','APPROVED'),
        ('rejected','REJECTED'),
    )
    name=models.CharField(max_length=30)
    email = models.EmailField(null=True, blank=True,default=None)
    pid=models.CharField(max_length=10,unique = True)
    phno=models.IntegerField()
    passw=models.CharField(max_length=30)
    cpassw=models.CharField(max_length=30)
    status=models.CharField(max_length=30,choices=STATUS_CHOICE,default='pending')


class drreg(models.Model):
    dimage=models.ImageField(upload_to='media/')
    dname=models.CharField(max_length=30)
    did=models.CharField(max_length=10)
    ddep=models.CharField(max_length=30)
    dphn=models.IntegerField()
    fee=models.CharField(max_length=30)
    demail=models.CharField(max_length=100)
    dpass=models.CharField(max_length=30)
    dpassre=models.CharField(max_length=30)
    
    def __str__(self):
        return f"{self.dname} - {self.did}"
    

class breg(models.Model):
    STATUS_CHOICE=(
        ('pending','PENDING'),
        ('approved','APPROVED'),
        ('rejected','REJECTED'),
    )
    name=models.CharField(max_length=30)
    pid=models.CharField(max_length=10)
    phno=models.IntegerField()
    dname=models.CharField(max_length=30)
    did=models.CharField(max_length=30)
    dphn=models.IntegerField()
    ddep=models.CharField(max_length=100)
    fee=models.CharField(max_length=30)
    bdate=models.CharField(max_length=30)
    btime=models.CharField(max_length=30)
    status=models.CharField(max_length=30,choices=STATUS_CHOICE,default='pending')

class lreg(models.Model):
    lname=models.CharField(max_length=30)
    lpass=models.CharField(max_length=30)

class labservice(models.Model):
    category=models.CharField(max_length=100)
    price=models.IntegerField()
    description=models.CharField(max_length=200)
    time=models.CharField(max_length=50)
    contact=models.CharField(max_length=10)

class lbreg(models.Model):
    name=models.CharField(max_length=30)
    pid=models.CharField(max_length=10)
    phno=models.IntegerField()
    category=models.CharField(max_length=30)
    price=models.IntegerField()
    description=models.CharField(max_length=300)
    time=models.CharField(max_length=100)
    lbdate=models.CharField(max_length=30)

class pay(models.Model):
    pid=models.CharField(max_length=30)
    name=models.CharField(max_length=30)
    email = models.EmailField()
    demail=models.EmailField()
    phno=models.CharField(max_length=20)
    did=models.CharField(max_length=30)
    dname=models.CharField(max_length=30)
    dphn=models.IntegerField()
    ddep=models.CharField(max_length=100)
    time = models.CharField(max_length=30)
    date= models.DateField(null=True)
    fee=models.CharField(max_length=30)

class labpay(models.Model):
    name=models.CharField(max_length=30)
    pid=models.CharField(max_length=10)
    phno=models.IntegerField()
    category=models.CharField(max_length=30)
    price=models.IntegerField()
    time=models.CharField(max_length=100)
    lbdate=models.CharField(max_length=30)
    result=models.ImageField(upload_to='media/')


class Bookdoctor(models.Model):
    doctor = models.ForeignKey(drreg, on_delete=models.CASCADE, null=True, blank=True)
    patient = models.ForeignKey(reg, on_delete=models.CASCADE, null=True, blank=True)
    TIME_CHOICES = (
        ('09:30 AM - 09:50 AM', '09:30 AM - 09:50 AM'),
        ('09:50 AM - 10:10 AM', '09:50 AM - 10:10 AM'),
        ('10:30 AM - 10:50 AM', '10:30 AM - 10:50 AM'),
        ('11:00 AM - 11:20 AM', '11:00 AM - 11:20 AM'),
        ('11:20 AM - 11:40 AM', '11:20 AM - 11:40 AM'),
        ('11:40 AM - 12:00 PM', '11:40 AM - 12:00 PM'),
        ('01:00 PM - 01:20 PM', '01:00 PM - 01:20 PM'),
        ('01:20 PM - 01:40 PM', '01:20 PM - 01:40 PM'),
        ('02:40 PM - 03:00 PM', '02:40 PM - 03:00 PM'),
        ('03:00 PM - 03:20 PM', '03:00 PM - 03:20 PM'),
        ('03:20 PM - 03:40 PM', '03:20 PM - 03:40 PM'),
        ('04:20 PM - 04:30 PM', '04:20 PM - 04:30 PM'),
    )
    time = models.CharField(max_length=255, choices=TIME_CHOICES)
    date = models.DateField(null=True)
    description = models.TextField()
    is_paid = models.BooleanField(default=False)
    email = models.EmailField()


# class Bookdoctor(models.Model):
#     doctor=models.ForeignKey(drreg,on_delete=models.CASCADE,null=True,blank=True)
#     patient=models.ForeignKey(reg,on_delete=models.CASCADE,null=True,blank=True)
#     TIME_CHOICES=(
#         ('10.00 AM - 10.10 AM', '10.00 AM - 10.10 AM'),
#         ('10.10 AM - 10.20 AM', '10.10 AM - 10.20 AM'),
#         ('10.20 AM - 10.30 AM', '10.20 AM - 10.30 AM'),
#         ('10.30 AM - 10.40 AM', '10.30 AM - 10.40 AM'),
#         ('10.40 AM - 10.50 AM', '10.40 AM - 10.50 AM'),
#         ('10.50 AM - 11.00 AM', '10.50 AM - 11.00 AM'),
#         ('11.00 AM - 11.10 AM', '11.00 AM - 11.10 AM'),
#         ('11.10 AM - 11.20 AM', '11.10 AM - 11.20 AM'),
#         ('11.20 AM - 11.30 AM', '11.20 AM - 11.30 AM'),
#         ('11.30 AM - 11.40 AM', '11.30 AM - 11.40 AM'),
#         ('11.40 AM - 11.50 AM', '11.40 AM - 11.50 AM'),
#         ('11.50 AM - 12.00 AM', '12.50 AM - 12.00 AM'),
#         ('12.00 AM - 12.10 AM', '12.00 AM - 12.10 AM'),
#         ('12.10 AM - 12.20 AM', '12.10 AM - 12.20 AM'),
#         ('12.20 AM - 11.30 AM', '12.20 AM - 12.30 AM'),
#     )
#     time=models.CharField(max_length = 255,choices=TIME_CHOICES)
#     date=models.DateField(null= True)
#     description=models.TextField()
#     is_paid = models.BooleanField(default = False)
#     email = models.EmailField()


