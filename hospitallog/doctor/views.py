from __future__ import unicode_literals
# ai import start 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from os import path
from PIL import Image

import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
import os 
from django.conf import settings
# Importing TextBlob
from textblob import TextBlob
csv_path=os.path.join(settings.BASE_DIR,'dataset','IMAReviewsPrivateDS.csv')
tweets = pd.read_csv(csv_path,encoding='latin1')
tweets.head()
# ai import end


# -*- coding: utf-8 -*-

from . models import reg,drreg,breg,lreg,labservice,pay,lbreg,labpay,Bookdoctor
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
import random
import string
# from twilio.rest import Client



from django.shortcuts import render,redirect
import razorpay #import this
from django.conf import settings
from django.http import HttpResponse

from django.http import JsonResponse #import this
from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt #import this
from django.http import HttpResponseBadRequest #import this
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# Create your views here.
def index(request):
    return render(request,'index.html')
def indexp(request):
    return render(request,'indexp.html')
def indexd(request):
    return render(request,'indexd.html')
def lablog(request):
    return render(request,'lablog.html')
def testimonial(request):
    return render(request,'testimonial.html')
def contact(request):
    return render(request,'contact.html')
def feature(request):
    return render(request,'feature.html')

def register(request):
    if request.method=="POST" :
        name = request.POST.get('name')
        phno = request.POST.get('phno')
        email=request.POST.get('email')
        passw = request.POST.get('passw')
        cpassw = request.POST.get('cpassw')
        pid = generate_unique_pid()
        reg(name=name,email=email,pid=pid,phno=phno,passw=passw,cpassw=cpassw).save()
        send_mail(
            subject = 'Your Unique ID',
            message = f'Dear {name},\n\nYour unique ID is: {pid}\n\nRegards,\nYour Application Team',
            from_email = settings.EMAIL_HOST_USER, 
            recipient_list = [email],  
        )
        return render(request,'index.html')
    else:
        return render(request,'register.html')

def generate_unique_pid():
    while True:
        pid = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))  # Generate a random 10-character string
        if not reg.objects.filter(pid=pid).exists():
            return pid

def login(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        passw = request.POST.get('passw')
        
        cr = reg.objects.filter(pid=pid, passw=passw)
        
        if cr.exists():
            user = cr.first()
            if user.status == "approved":
                request.session['pid'] = user.pid
                return render(request, 'indexp.html')
            else:
                # If user status is not approved, render login form with custom error message
                return render(request, 'login.html', {'error_message': 'Your account is not approved.'})
        else:
            # If no matching record found, render login form with custom error message
            return render(request, 'login.html', {'error_message': 'Invalid credentials.'})
    else:
        return render(request, 'login.html')

def profile(request):
    ownername=request.session['pid']
    cr=reg.objects.get(pid=ownername)
    name=cr.name
    patient_id=cr.pid
    phone_number=cr.phno
    password=cr.passw
    return render(request,'profile.html',{'name':name,'pid':patient_id,'phno':phone_number,'passw':password})

def profiled(request):
    ownername=request.session['did']
    cr=drreg.objects.get(did=ownername)
    dimage = cr.dimage
    dname=cr.dname
    ddep=cr.ddep
    did=cr.did
    fee=cr.fee
    demail=cr.demail
    phone_number=cr.dphn
    password=cr.dpass
    return render(request,'profiled.html',{'dimage':dimage,'dname':dname,'ddep':ddep,'did':did,'dphn':phone_number,'dpass':password,'fee':fee,'demail':demail})

def update(request):
    ownername=request.session['pid']
    cr=reg.objects.get(pid=ownername)
    name=cr.name
    patient_id=cr.pid
    phone_number=cr.phno
    password=cr.passw
    return render(request,'updateprofile.html',{'name':name,'pid':patient_id,'phno':phone_number,'passw':password})


def proupdate(request):
    ownername=request.session['pid']
    if request.method=="POST":
        name=request.POST.get('name')
        phno=request.POST.get('phno')
        passw=request.POST.get('passw')

        data=reg.objects.get(pid=ownername)
        data.name=name
        data.phno=phno
        data.passw=passw
        data.save()
        return render(request,'index.html')
    else:
        return render(request,'updateprofile.html')

def dreg(request):
    if request.method=="POST" :
        dimage = request.FILES['dimage']
        dname = request.POST.get('dname')
        did = request.POST.get('did')
        ddep = request.POST.get('ddep')
        dphn = request.POST.get('dphn')
        fee = request.POST.get('fee')
        demail= request.POST.get('demail')
        dpass = request.POST.get('dpass')
        dpassre = request.POST.get('dpassre')
        drreg(dimage=dimage,dname=dname,did=did,demail=demail,ddep=ddep,dphn=dphn,fee=fee,dpass=dpass,dpassre=dpassre).save()
        return redirect(dlog)
    else:
        return render(request,'dreg.html')
    
def dlog(request):
    if request.method=='POST':
        did=request.POST.get('did')
        dpass=request.POST.get('dpass')
        cr=drreg.objects.filter(did=did,dpass=dpass)
        if cr:
            user=drreg.objects.get(did=did,dpass=dpass)
            id=user.id
            did=user.did
            dpass=user.dpass
            request.session['did']=did
            request.session['email']=user.demail
            n=request.session['email']
            print(n)
            return redirect(indexd)
        else:
            return render(request,'dlogin.html')
    else:
        return render(request,'dlogin.html')
    
def listdr(request):
    cr=drreg.objects.all()
    return render(request,'listdr.html',{'a':cr})

def book(request):
    if request.method=='POST':
        id=request.POST.get('id')
        sd=drreg.objects.get(id=id)
        name=sd.dname
        phn=sd.dphn
        dep=sd.ddep
        did=sd.did
        fee=sd.fee
        pid=request.session['pid']
        cr=reg.objects.get(id=id)
        a=cr.name
        b=cr.pid
        c=cr.phno    
    return render(request,'booking.html',{'name':a,'pid':b,'phno':c,'dname':name,'fee':fee,'dphn':phn,'ddep':dep,'did':did})

def booking(request):
    if request.method=='POST':
        name=request.POST.get('name')
        pid=request.POST.get('pid')
        phno = request.POST.get('phno')
        dname = request.POST.get('dname')
        dphn = request.POST.get('dphn')
        did = request.POST.get('did')
        ddep = request.POST.get('ddep')
        fee = request.POST.get('fee')
        bdate = request.POST.get('bdate')
        btime = request.POST.get('btime')
        breg(name=name,pid=pid,phno=phno,dname=dname,dphn=dphn,ddep=ddep,did=did,fee=fee,bdate=bdate,btime=btime).save()
        return render(request,'indexp.html')
    else:
        return render(request,'booking.html')
    
def listuser(request):
    did=request.session['did']
    cr=pay.objects.filter(did=did)
    return render(request,'listuser.html',{'a':cr})

def alog(request):
    if request.method=='POST':
        uname = request.POST.get('username')
        passw = request.POST.get('apass')
        u = 'admin'
        p = 'admin'
        if uname==u:
            if passw==p:
                return render(request,'indexa.html')
            else:
                return render(request,"alog.html")
        else:
            return render(request,"alog.html")
    else:
        return render(request,"alog.html")

def alistusers(request):
    cr=reg.objects.all()
    return render(request,'alistusers.html',{'b':cr})

def alistdoctors(request):
    cr=drreg.objects.all()
    return render(request,'alistdoctors.html',{'c':cr})

def alistlab(request):
    cr=lreg.objects.all()
    return render(request,'alistlab.html',{'d':cr})

def lablog(request):
    if request.method=='POST':
        uname = request.POST.get('username')
        passw = request.POST.get('lpass')
        u = 'kslab'
        p = 'kslab'
        if uname==u:
            if passw==p:
                return render(request,'indexl.html')
            else:
                return render(request,"lablog.html")
        else:
            return render(request,"lablog.html")
    else:
        return render(request,"lablog.html")
    
def ed(request):
    if request.method=='POST':
        id=request.POST.get('id')
        sd=breg.objects.get(id=id)
        id=sd.id
        name=sd.name
        phno=sd.phno
        pid=sd.pid   
        bdate=sd.bdate
        btime=sd.btime
        status=sd.status
    return render(request,'ed.html',{'id':id,'name':name,'pid':pid,'phno':phno,'bdate':bdate,'btime':btime,'status':status })

def update(request):
    if request.method=='POST':
        name=request.POST.get('name')
        pid=request.POST.get('pid')
        phno = request.POST.get('phno')
        bdate = request.POST.get('bdate')
        btime = request.POST.get('btime')
        status = request.POST.get('status')
        id=request.POST.get('id')
        dt=breg.objects.get(id=id)
        dt.name=name
        dt.pid=pid
        dt.phno=phno
        dt.bdate=bdate
        dt.btime=btime
        dt.status=status
        dt.save()
        return render(request,'indexd.html')
    
def mybookings(request):
    pid=request.session['pid']
    try:
        # j=reg.objects.filter(pid=pid)
        cr = Bookdoctor.objects.filter(patient__pid=pid)
        print(cr)
        return render(request,'mybookings.html',{'cr':cr})
    except reg.DoesNotExist:
        return redirect('login')

def labbook(request):
    pid=request.session['pid']
    cr=lbreg.objects.filter(pid=pid)
    return render(request,'labbook.html',{'a':cr})

def adupdate(request):
    if request.method=='POST':
        name=request.POST.get('name')
        pid=request.POST.get('pid')
        phno = request.POST.get('phno')
        status = request.POST.get('status')
        id=request.POST.get('id')
        dt=reg.objects.get(id=id)
        dt.name=name
        dt.pid=pid
        dt.phno=phno
        dt.status=status
        dt.save()
        return render(request,'indexa.html')
    
def ad(request):
    if request.method=='POST':
        id=request.POST.get('id')
        sd=reg.objects.get(id=id)
        id=sd.id
        name=sd.name
        phno=sd.phno
        pid=sd.pid  
        status=sd.status
    return render(request,'ad.html',{'id':id,'name':name,'pid':pid,'phno':phno,'status':status})

def labservices(request):
    if request.method=="POST" :
        category = request.POST.get('category')
        price = request.POST.get('price')
        description = request.POST.get('description')
        time = request.POST.get('time')
        contact = request.POST.get('contact')
        labservice(category=category,price=price,description=description,contact=contact,time=time).save()
        return render(request,'indexl.html')
    else:
        return render(request,'labservices.html')
    
def labselect(request):
    cr=labservice.objects.all()
    return render(request,'labselect.html',{'a':cr})

def booklab(request):
    if request.method=='POST':
        id=request.POST.get('id')
        sd=labservice.objects.get(id=id)
        category=sd.category
        price=sd.price
        description=sd.description
        time=sd.time
        pid=request.session['pid']
        cr=reg.objects.get(pid=pid)
        a=cr.name
        b=cr.pid
        c=cr.phno    
    return render(request,'bookinglab.html',{'name':a,'pid':b,'phno':c,'category':category,'price':price,'description':description,'time':time})

def bookinglab(request):
    if request.method=='POST':
        name=request.POST.get('name')
        pid=request.POST.get('pid')
        phno = request.POST.get('phno')
        category=request.POST.get('category')
        price=request.POST.get('price')
        description = request.POST.get('description')
        time = request.POST.get('time')
        lbdate = request.POST.get('lbdate')
        lbreg(name=name,pid=pid,phno=phno,category=category,price=price,description=description,time=time,lbdate=lbdate).save()
        return render(request,'indexp.html')
    else:
        return render(request,'bookinglab.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Bookdoctor
from razorpay import Client as RazorpayClient

razorpay_client = RazorpayClient(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def payment(request,id):
    pid=request.session['pid']

    cr=Bookdoctor.objects.filter(patient__pid=pid)
    totalprice = 0
    if not cr.exists():
        return render(request,'your_template.html')
    
    
    for i in cr:
     pay(name=i.patient.name, email= i.email ,demail=i.doctor.demail,time=i.time,date=i.date,pid=i.patient.pid, phno=i.patient.phno, did=i.doctor.did, dname=i.doctor.dname,dphn=i.doctor.dphn,ddep=i.doctor.ddep,fee=i.doctor.fee).save()
     totalprice += int(i.doctor.fee)
     i.delete()
    
    totalprice = int(totalprice*100)
    amount=int(totalprice)
    #amount=200
    print('amount is',str(amount))
    currency = 'INR'
    #amount = 20000  # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    return render(request, 'Payment.html', context=context)



 
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'pay_success.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'pay_failed.html')
            else:
 
                # if signature verification fails.
                return render(request, 'pay_failed.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
 
@csrf_exempt
def paymenthandler1(request):
    
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'pay_success.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'pay_failed.html')
            else:
 
                # if signature verification fails.
                return render(request, 'pay_failed.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
    



def payment1(request):
    pid=request.session['pid']

    cr=lbreg.objects.filter(pid=pid)
    totalprice = 0
    # if not cr.exists():
    #     return render(request,'your_template.html')
    
    
    for i in cr:
     labpay(name=i.name,pid=i.pid,price=i.price,lbdate=i.lbdate,category=i.category,phno=i.phno).save()
     totalprice += int(i.price)
     i.delete()
    
    totalprice = int(totalprice*100)
    amount=int(totalprice)
    #amount=200
    print('amount is',str(amount))
    currency = 'INR'
    # amount = 20000  # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler1/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    return render(request, 'payment1.html', context=context)


@csrf_exempt
def paymenthandler1(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                                        
                    # render success page on successful caputre of payment
                    return render(request, 'pay_success.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'pay_failed.html')
            else:
 
                # if signature verification fails.
                return render(request, 'pay_failed.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
    
def lablistusers(request):
    lb=labpay.objects.all()
    return render(request,'lablistusers.html',{'a':lb})

def uploadresult(request):
    if request.method=='POST':
        id=request.POST.get('id')
        sd=labpay.objects.get(id=id)
        id=sd.id
        name=sd.name
        result=sd.result
    return render(request,'upload.html',{'id':id,'name':name,'result':result})

def upload(request):
    if request.method=='POST':
        name=request.POST.get('name')
        result = request.FILES['result']
        id=request.POST.get('id')
        dt=labpay.objects.get(id=id)
        dt.name=name
        dt.result=result
        dt.save()
        return render(request,'indexl.html')
  
def labresult(request):
    pid=request.session['pid']
    cr=labpay.objects.filter(pid=pid)
    return render(request,'labresult.html',{'a':cr})

def resultview(request):
    pid=request.session['pid']
    cr=labpay.objects.filter(pid=pid)
    return render(request,'resultview.html',{'a':cr})



def BookdoctorView(request):
    if 'pid' in request.session:
        pid = request.session['pid']
        try:
            pt = reg.objects.get(pid=pid)
            d = drreg.objects.all()
            available_timeslots = []
            # Initialize as an empty list

            if request.method == 'POST':
                dname = request.POST.get('dname')
                date = request.POST.get('date')
                email = request.POST.get('email')
                description = request.POST.get('description')
                pname = pt
                doctor_instance = drreg.objects.get(dname=dname)

                # Get all existing bookings for the selected date
                existing_bookings = Bookdoctor.objects.filter(doctor=doctor_instance, date=date)

                # Get all available timeslots for the selected date
                for choice in Bookdoctor.TIME_CHOICES:
                    if choice[0] not in existing_bookings.values_list('time', flat=True):
                        available_timeslots.append(choice)
                        # Append as a tuple

                if request.POST.get('time') in [choice[0] for choice in available_timeslots]:
                    # If the selected timeslot is available, create a new booking
                    time = request.POST.get('time')
                    Bookdoctor(doctor=doctor_instance, patient=pname, time=time, date=date, description=description, email=email).save()
                    return render(request, 'indexp.html')
                else:
                    # If the selected timeslot is not available, return to the booking form with a message
                    return HttpResponse('This timeslot is already taken. Please choose another time.')

            else:
                return render(request, 'docbooking.html', {'pt': pt, 'd': d, 'available_timeslots': Bookdoctor.TIME_CHOICES})

        except reg.DoesNotExist:
            return redirect('login')
    else:
        return redirect(login)


def bookedView(request):
    if 'pid' in request.session:
        pid=request.session['pid']
        try:
            f=reg.objects.get(pid=pid)
            l=pay.objects.filter(pid=pid)
            return render(request,'viewbookings.html',{'l':l})
        
        except reg.DoesNotExist:
            return redirect('login')
    
    else:
        return redirect('login')
    
    
def meetingView(request):
    if 'did' or 'pid' in request.session:
        did = request.session['did'] 
        uid= request.session['pid']
        try:
            user = pay.objects.filter(did=did)
            name = user.dname
            email = user.email
            print(name)
            return render(request,'meetings.html',{'name':name, 'email':email})
        except :
            
            print(uid)
            user= pay.objects.get(pid=uid)
            name = user.dname
            email = user.email
            return render(request,'meetings.html',{'name':name, 'email':email})
    else:
        return HttpResponse('error')
    
@csrf_exempt      
def send_room_id(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))  # Parse JSON data from request body
            email = data.get('email')
            room_id = data.get('room_id')
            url = data.get('url')

            print('Email:', email)
            print('Room ID:', room_id)

            # Construct the email content
            subject = 'Your Meeting Room ID'
            message = f'Dear User,\n\nYour room ID for the meeting is: {room_id}\n\nYou can join the meeting using the following link:\n{url}\n\nBest regards,\nYour Organization'

            # Send the email
            send_mail(
                subject,
                message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],  # Recipient's email address
                fail_silently=False,
            )

            return JsonResponse({'success': True})
        except Exception as e:
            # Log any exceptions that occur during email sending
            print('Error sending email:', str(e))
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


# AI Code Start

def DoctorPredictView(request):
    result = None
   
    nltk.download('stopwords')
    if request.method == 'POST':
        department_name=request.POST.get('department_name')
        tweets.reviews = tweets.reviews.str.replace('[#,@,&]', '')
        #Remove twitter handlers
        tweets.reviews = tweets.reviews.str.replace('@[^\s]+','')
        #Remove digits
        tweets.reviews = tweets.reviews.str.replace(' \d+ ','')
        # remove multiple spaces with single space
        tweets.reviews = tweets.reviews.str.replace("http\S+", "")
        # remove multiple spaces with single space
        tweets.reviews = tweets.reviews.str.replace('\s+', ' ')
        #remove all single characters
        tweets.reviews = tweets.reviews.str.replace(r'\s+[a-zA-Z]\s+', '')
        nltk.download('punkt')
        stop_words = stopwords.words('english')
        stop_words.extend(['ha', 'wa', '-'])

        # Get a string of tweets
        # tweet_text = ",".join(review.lower() for review in tweets.reviews if 'covid' not in review)
        
        tweet_text = ",".join(review.lower() for review in tweets.reviews if not isinstance(review, float) and 'covid' not in review)


        # Create and generate a word cloud image:
        wordcloud = WordCloud(max_font_size=50,
                            max_words=100,
                            stopwords=stop_words,
                            scale=5,
                            background_color="white").generate(tweet_text)
        # Display the generated image:
        # plt.figure(figsize=(10,7))
        # plt.imshow(wordcloud, interpolation='bilinear')
        # plt.axis("off")
        # plt.title('Most repeated words in reviews',fontsize=15)
        # plt.show()
        positive_reviews = tweets[tweets['tag'] == 'positive']
        negative_reviews = tweets[tweets['tag'] == 'negative']
        # Count the number of positive and negative reviews
        positive_count = len(positive_reviews)
        negative_count = len(negative_reviews)

        # Data for the pie chart
        # labels = ['Positive Reviews', 'Negative Reviews']
        # sizes = [positive_count, negative_count]
        # colors = ['#66b3ff', '#ff9999']  # Blue for positive, red for negative
        # explode = (0.1, 0)  # Explode the first slice (positive reviews)

        # Plotting the pie chart
        # plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        # plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular
        # plt.show()
        doctors_in_department = tweets[tweets['department'] == department_name]['dname'].unique()
        print(f"Doctors in the {department_name} department:")
        best_recommendation_score=0
        
        def analyze_sentiment(review):
            analysis = TextBlob(str(review))
            return analysis.sentiment.polarity
        
        all_doctors = [] 
        # Filter reviews for the specified doctor
        for doctor in doctors_in_department:
            print(doctor)
            doctor_reviews = tweets[tweets['dname'] == doctor]['reviews']

        # Analyze sentiment for each review
            sentiments = doctor_reviews.apply(analyze_sentiment)
        # sentiments = [analyze_sentiment(review) for review in doctor_reviews]

        # Calculate recommendation score
            recommendation_score = sentiments.mean()
        # recommendation_score = sum(sentiments) / len(sentiments)
            if recommendation_score > best_recommendation_score:
                best_recommendation_score = recommendation_score
                best_doctor = doctor
            all_doctors.append(doctor)

        # Visualize sentiment distribution in a pie chart
        # positive_count = len(sentiments[sentiments > 0])
        # negative_count = len(sentiments[sentiments < 0])
        # neutral_count = len(sentiments[sentiments == 0])

        # Data for the pie chart
        # labels = ['Positive', 'Negative', 'Neutral']
        # sizes = [positive_count, negative_count, neutral_count]
        # colors = ['#66b3ff', '#ff9999', '#99ff99']  # Blue for positive, red for negative, green for neutral
        # explode = (0.1, 0, 0)  # Explode the first slice (positive sentiment)

        # Plotting the pie chart
        # plt.figure(figsize=(8, 8))
        # plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        # plt.title(f'Sentiment Distribution for {department_name}\'s Reviews')
        # plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular

        # Display the pie chart
        # plt.show()
        # scores = [TextBlob(review).sentiment.polarity for review in doctor_reviews]

        # chart_data = {
        #     'labels': [f'Review {i+1}' for i in range(len(doctor_reviews))],
        #     'scores': scores
        # }


        # Print the recommendation score and interpretation
        print('Best doctor is : ',best_doctor)
        print('The Recommendation Score is : ',best_recommendation_score)
        dept_name = department_name
        doc = best_doctor
        alldoc=all_doctors

        # Interpret recommendation score
        if recommendation_score > 0:
            result="Overall positive sentiment is : High recommendation!"
        elif recommendation_score < 0:
            result="Overall negative sentiment: Caution advised."
        else:
            result="Neutral sentiment. Consider other factors for recommendation."
        return render(request, 'predictionresult.html', {'result': result,'doc':doc,'alldoc':alldoc,'dept_name':dept_name})
    return render(request, 'prediction.html', {'result': result})

def PredictionResultView(request):
    return render(request, 'predictionresult.html')


import random
import csv
def FeedbackUploadView(request):
    if request.method == 'POST':
        reviews = request.POST.get('reviews')
        tag = request.POST.get('tags')
        selected_doctor_id = request.POST.get('doctor')  
        
        selected_doctor = drreg.objects.get(id=selected_doctor_id)
        dname = selected_doctor.dname
        department = selected_doctor.ddep

        while True:
            random_number = random.randint(500, 600)
            pid = random_number

            csv_file_path = os.path.join(settings.BASE_DIR,'dataset','IMAReviewsPrivateDS.csv')
            with open(csv_file_path, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    existing_pid = str(row[0]) 
                    if existing_pid == pid:
                        break
                else:
                   
                    break

       
        with open(csv_file_path, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([pid, reviews, tag,dname, department])

        return redirect('indexp')  
    
    doctors = drreg.objects.all()
    return render(request, 'feedbackupload.html', {'doctors': doctors})





# AI Code End
    
