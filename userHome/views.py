from django.http import HttpResponse
from django.shortcuts import render, redirect
from adminHome.models import Futsal
from django.contrib.auth import logout
from adminHome.models import Futsal, Booking
from userAuth.models import User
from datetime import datetime, timedelta
from django.contrib import messages
from .forms import FutsalSearchForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from adminHome.forms import AddFutsalForm
from django.shortcuts import render, redirect
from django.conf import settings
import requests
import json
from django.db.models import Count
from adminHome.utils import find_most_booked_futsal_for_week



def homePage(request):
    futsals = Futsal.objects.all()
    total_futsals = Futsal.objects.count()
    form = FutsalSearchForm()
    futsal_types = Futsal.objects.values_list('futsal_type', flat=True).distinct()
    
    most_booked_futsal, num_bookings = find_most_booked_futsal_for_week()
    print(most_booked_futsal, num_bookings)


    if request.user.is_authenticated:
        user_booked_futsals = Booking.objects.filter(user=request.user)
        user_booked_count = Booking.objects.filter(user=request.user).count()
    else:
        user_booked_futsals = None
    context = {
        'futsals': futsals,
        'total_futsals': total_futsals,
        'futsal_types': futsal_types,
        'user_booked_futsals': user_booked_futsals,
        'user_booked_count': user_booked_count,
        'most_booked_futsal': most_booked_futsal,
        'form': form,
    }

    return render (request, 'userHome/home.html', context) 


# def futsalPage(request):
#     futsals = Futsal.objects.all()
#     form = FutsalSearchForm()

#     if request.user.is_authenticated:
#         user_booked_futsals = Booking.objects.filter(user=request.user)
#     else:
#         user_booked_futsals = None

#         for futsal in user_booked_futsals:
#             print(futsal.futsal)

#     context = {
#         'futsals': futsals,
#         'user_booked_futsals': user_booked_futsals,
#         'form': form, 
#     }
#     return render (request, 'userHome/futsal_list.html', context)


def bookFutsal(request, pk):
    futsal = Futsal.objects.get(id=pk)
    if request.user.is_authenticated:
        user_booked_futsals = Booking.objects.filter(user=request.user)
    else:
        user_booked_futsals = None

    time_slots = []
    book_time = 1
    print(futsal.open_time , futsal.close_time)
    while futsal.open_time <= futsal.close_time:
        time_slots.append(futsal.open_time.strftime("%I:%M %p"))
        futsal.open_time = futsal.open_time.replace(hour=futsal.open_time.hour + book_time)

    if request.method == 'POST':
        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')
        book_time_str = request.POST.get('book_time')
        book_time = int(book_time_str)
        total_price = book_time * futsal.price
        print(booking_date, booking_time, book_time)
        try:
            booking = Booking.objects.create(
            user=request.user,
            futsal=Futsal.objects.get(id=pk),
            booking_date=booking_date,
            booking_time=booking_time,
            book_time=book_time,
            total_price=total_price
        )
            messages.success(request, f' {'Successfully Booked at ' + booking.futsal.name }')
            return redirect('/futsal_list/')
        except Exception as e:
            raise Exception("Booking Failed" + str(e))
            return redirect('futsal_list/')

    context = {
        'futsal': futsal,
        'time_slots': time_slots,
        'user_booked_futsals': user_booked_futsals,

    }
    return render(request, 'userHome/checkout.html', context)

def futsal_section(request):
    futsals = Futsal.objects.all()

def logoutUser(request):
    logout(request)
    return redirect('login')


def myBookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-id')
    if request.user.is_authenticated:
        user_booked_futsals = Booking.objects.filter(user=request.user)


    print(bookings)
    context = {
        'bookings': bookings,
        'user_booked_futsals':  user_booked_futsals,
    }
    return render(request, 'userHome/my_bookings.html', context)


def topBooked(request):
    topBooked = Booking.object.filter()

def searchFutsal(request):
    print("hello")
    form = FutsalSearchForm()
    if request.method == 'POST':
        form = FutsalSearchForm(request.POST)

    if form.is_valid():
        search_query = form.cleaned_data.get('search')
        name = form.cleaned_data.get('name')
        location = form.cleaned_data.get('location')
        futsal_type = form.cleaned_data.get('futsal_type')
        price = form.cleaned_data.get('price')

        # Filter Futsal objects based on the search criteria
        futsals = Futsal.objects.filter(
            name__icontains=search_query,
            location__icontains=location,
            futsal_type__icontains=futsal_type,
            price__lte=price,
            # Add more filters as needed
        )

        # You can customize the search logic based on your requirements

        context = {'futsals': futsals, 'form': form}
        return render(request, 'userHome/search_response.html', context)

    context = {'form': form}
    return render(request, 'userHome/home.html', context)


def futsalPage(request):
    futsals = Futsal.objects.all()
    form = FutsalSearchForm()

    if request.user.is_authenticated:
        user_booked_futsals = Booking.objects.filter(user=request.user)
    else:
        user_booked_futsals = None

    context = {
        'futsals': futsals,
        'user_booked_futsals': user_booked_futsals,
        'form': form, 
    }

    return render(request, 'userHome/futsal_list.html', context)


def cancelBooking(request, pk):
    booking = Booking.objects.get(id=pk)
    try:
        booking.delete()
        messages.success(request, f'Booking Cancelled')
    except Exception as e:
        raise Exception("Booking Cancellation Failed" + str(e))
    
    return redirect('my_bookings')

def manageFutsal(request):
    futsals = Futsal.objects.filter(addedBy=request.user)
    futsal_form = AddFutsalForm()

    if request.method == 'POST':
        print('Hello')
        futsal_form = AddFutsalForm(request.POST, request.FILES)
        if futsal_form.is_valid():
            futsal = futsal_form.save(commit=False)
            print(f"Before setting addedBy: {futsal.addedBy}")  # Debugging line
            futsal.addedBy = request.user
            print(f"After setting addedBy: {futsal.addedBy}")  # Debugging line
            futsal.save()
            return redirect('manage_futsal')

    context = {
        'futsals': futsals,
        'futsal_form': futsal_form,
    }
    return render(request, 'userHome/futsal_owner_table.html', context)

@login_required
def initiate_payment(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    user_detail = User.objects.get(username=request.user)
    print("Detail of user",user_detail)
    print("UD",request.user.email)
    booking_info = {
        "futsal_name": booking.futsal.name,
        "booking_date": booking.booking_date.strftime("%d-%m-%Y"),
        "booking_time": booking.booking_time.strftime("%I:%M %p"),
        "book_time": str(booking.book_time),
        "status": booking.status,
        "total_price": str(booking.total_price),
    }
    booking_price = float(booking_info["total_price"]) * 100
    
    print("Booking Price",booking_price)
    print("Booking ID",booking_id)
    if request.user != booking.user:
        return redirect('login')  

    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    payload = json.dumps({
        "return_url": "http://localhost:8000/payment_detail/",
        "website_url": "https://example.com/",
        "amount": str(booking_price),
        "purchase_order_id": str(booking_id),
        "purchase_order_name": "test",
        "customer_info": {
        "name": str(request.user),
        "email": str(request.user.email),
        "phone": str(request.user.phone)
         }
    })
    headers = {
        'Authorization': 'key live_secret_key_68791341fdd94846a146f0457ff7b455',
        'Content-Type': 'application/json',
    }

    try:
        # response = requests.post(url, headers=headers, json=payload)
        # print(response)
        # response_data = response.json()
        # if response_data['token']:
        #     return redirect(response_data['redirect_url'])
        # else:
        #     # Handle payment initiation failure
        #     return render(request, 'payment_error.html', {'error_message': response_data.get('message')})
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        response_data = json.loads(response.text)
        payment_url = response_data.get('payment_url')
        return redirect(payment_url)
    except requests.RequestException as e:
        # Handle request exception
        return render(request, 'payment_error.html', {'error_message': str(e)})


def payment_detail(request):
    pidx = request.GET.get('pidx')
    transaction_id = request.GET.get('transaction_id')
    tidx = request.GET.get('tidx')
    amount = request.GET.get('amount')
    total_amount = int(request.GET.get('total_amount')) / 100
    mobile = request.GET.get('mobile')
    status = request.GET.get('status')
    purchase_order_id = request.GET.get('purchase_order_id')
    purchase_order_name = request.GET.get('purchase_order_name')

    try:
        booking_instance = Booking.objects.get(id=purchase_order_id)
    except Booking.DoesNotExist:
        return HttpResponse("Booking not found", status=404)

    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    payload = json.dumps({
        "pidx": pidx
    })
    headers = {
        'Authorization': 'key live_secret_key_68791341fdd94846a146f0457ff7b455',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_data = json.loads(response.text)
    print("Response: ", response_data)

    if response_data.get('status') == 'Completed':
        booking_instance.payment_status = 'Completed'
        booking_instance.pidx = response_data.get('pidx')
        booking_instance.save()

        context = {
            'pidx': response_data.get('pidx'),
            'transaction_id': response_data.get('transaction_id'),
            'tidx': tidx,
            'amount': amount,
            'total_amount': total_amount,
            'mobile': mobile,
            'status': response_data.get('status'),
            'fee': response_data.get('fee'),
            'refunded': response_data.get('refunded'),
            'purchase_order_id': purchase_order_id,
            'purchase_order_name': booking_instance.futsal.name,  # Corrected the reference
            'futsal_img': booking_instance.futsal.images.url,  # Corrected the reference
            'booking': booking_instance
        }
        return render(request, 'userHome/payment_detail.html', context)
    else:
        print("Payment not completed")
        return HttpResponse("Payment not completed", status=400)

def view_bill(request, booking_id):
    booking_instance = Booking.objects.get(id = booking_id)
    print(booking_instance.pidx)
    pidx = booking_instance.pidx
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    payload = json.dumps({
        "pidx": pidx
    })
    headers = {
        'Authorization': 'key live_secret_key_68791341fdd94846a146f0457ff7b455',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_data = json.loads(response.text)
    print("Response: ", response_data)
    mobile = request.user.phone
    amount = response_data.get('total_amount') / 100
    tidx = 'sdasda'
    context = {
            'pidx': response_data.get('pidx'),
            'transaction_id': response_data.get('transaction_id'),
            'tidx': tidx,
            'amount': amount,
            'total_amount': amount,
            'mobile': mobile,
            'status': response_data.get('status'),
            'fee': response_data.get('fee'),
            'refunded': response_data.get('refunded'),
            'purchase_order_id': str(booking_id),
            'purchase_order_name': booking_instance.futsal.name,  # Corrected the reference
            'futsal_img': booking_instance.futsal.images.url,  # Corrected the reference
            'booking': booking_instance
    }
    return render(request, 'userHome/payment_detail.html', context)