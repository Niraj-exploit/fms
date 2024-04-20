from django.shortcuts import render, redirect
from .models import Booking, Futsal
from django.db import models
from .forms import AddFutsalForm, UserCreationForm
from userAuth.models import User
from django.shortcuts import get_object_or_404
from .utils import calculate_total_money_earned_by_futsals, find_most_booked_futsal_for_week
def dashboard(request):
    total_users = get_total_users()
    total_bookings = get_total_bookings()
    total_futsals = get_total_futsals()
    total_money_earned_by_futsals = calculate_total_money_earned_by_futsals()
    total_money_earned = sum(total_money_earned_by_futsals.values())
    most_booked_futsal_for_week = find_most_booked_futsal_for_week()
    print(total_money_earned_by_futsals)

    context = {
        'total_users': total_users,
        'total_bookings': total_bookings,
        'total_futsals': total_futsals,
        'total_money_earned_by_futsals': total_money_earned_by_futsals,
        'total_money_earned': total_money_earned,
        'most_booked_futsal_for_week': most_booked_futsal_for_week
    }

    return render(request, 'adminHome/dashboard.html', context)

def get_total_users():
    # return Booking.objects.values('user').annotate(user_count=models.Count('user')).count()
    return User.objects.count()

def get_total_bookings():
    return Booking.objects.count()

def get_total_futsals():
    return Futsal.objects.count()

def tablePage(request):
    futsals = Futsal.objects.all()
    bookings = Booking.objects.all()
    futsal_form = AddFutsalForm()
    context = {
        'futsals': futsals,
        'bookings': bookings,
        'futsal_form': futsal_form,
    }
    return render(request, 'adminHome/tables.html', context)

def bookingPage(request): 
    bookings = Booking.objects.all()


    context = {
        'bookings': bookings,
        'total_money_earned_by_futsals': total_money_earned_by_futsals
    }
    return render(request, 'adminHome/booking.html', context)

def addFutsal(request):
    if request.method == 'POST':
        form = AddFutsalForm(request.POST, request.FILES)
        print(request.user)
        if form.is_valid():
            form.addedBy = request.user
            form.save()
            return redirect('table')
        else:
            form = AddFutsalForm()
    return render(request, 'adminHome/table.html', {'form': form})

def approveBooking(request, pk):
    booking = Booking.objects.get(id=pk)
    booking.status = 'Approved'
    booking.save()
    return redirect('table')

def rejectBooking(request, pk):
    booking = Booking.objects.get(id=pk)
    booking.status = 'Rejected'
    booking.save()
    return redirect('table')

def completeBooking(request, pk):
    booking = Booking.objects.get(id=pk)
    booking.status = 'Completed'
    booking.save()
    return redirect('table')

def manage_user_view(request):
    users = User.objects.all().order_by('-id')

    if request.method == 'POST':
        if 'edit' in request.POST:
            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, pk=user_id)
            form = UserCreationForm(request.POST, instance=user)
        else:
            form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = UserCreationForm()
    context = {
        'users' : users,
        'form' : form
    }

    return render( request, 'adminHome/manage_users.html', context)

