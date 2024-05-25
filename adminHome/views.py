from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking, Futsal
from django.db import models
from .forms import AddFutsalForm, UserCreationForm
from userAuth.models import User
from .utils import calculate_total_money_earned_by_futsals, find_most_booked_futsal_for_week
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from .decorators import admin_required
from django.contrib import messages


@admin_required
@login_required
def dashboard(request):
    total_users = get_total_users()
    total_bookings = get_total_bookings()
    total_futsals = get_total_futsals()
    total_money_earned_by_futsals = calculate_total_money_earned_by_futsals()
    total_money_earned = sum(total_money_earned_by_futsals.values())
    most_booked_futsal_for_week = find_most_booked_futsal_for_week()
    print(most_booked_futsal_for_week)

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

@admin_required
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

@admin_required
def bookingPage(request): 
    bookings = Booking.objects.all()


    context = {
        'bookings': bookings,
    }
    return render(request, 'adminHome/booking.html', context)

@admin_required
@login_required
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

@admin_required
@login_required
def approveBooking(request, pk):
    booking = Booking.objects.get(id=pk)
    booking.status = 'Approved'
    booking.save()
    return redirect('table')

@admin_required
@login_required
def rejectBooking(request, pk):
    booking = Booking.objects.get(id=pk)
    booking.status = 'Rejected'
    booking.save()
    return redirect('table')

@admin_required
@login_required
def completeBooking(request, pk):
    booking = Booking.objects.get(id=pk)
    booking.status = 'Completed'
    booking.save()
    return redirect('table')

@admin_required
@login_required
def manage_user_view(request):
    print("Hello")
    users = User.objects.all().order_by('-id')
    print(users)
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_user_view')

    context = {
        'users': users,
        'form': form
    }

    return render(request, 'adminHome/manage_users.html', context)

@admin_required
@login_required
def update_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    form = UserCreationForm(instance=user)

    if request.method == 'POST':
        form = UserCreationForm(request.POST, instance=user)
        if form.is_valid():
            new_password = form.cleaned_data.get('password')
            if new_password:
                user.set_password(new_password) 
            else:
                form.cleaned_data.pop('password', None)
            form.save()
            return redirect('manage_user_view')

    context = {'form': form}
    return render(request, 'adminHome/update_user.html', context)

@admin_required
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return redirect('manage_user_view')

@admin_required
@login_required
def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    bookings = Booking.objects.filter(user=user)
    context = {
        'user': user,
        'bookings': bookings
    }
    return render(request, 'adminHome/user_detail.html', context)

@admin_required
@login_required
def update_futsal(request, futsal_id):
    futsal = get_object_or_404(Futsal, id=futsal_id)  
    if request.method == 'POST':
        form = AddFutsalForm(request.POST, instance=futsal)
        if form.is_valid():
            form.save()
            return redirect('/admin/tables/') 
    else:
        form = AddFutsalForm(instance=futsal)
    return render(request, 'adminHome/update_futsals.html', {'form': form})

@admin_required
@login_required
def delete_futsal(request, futsal_id):
    futsal = get_object_or_404(Futsal, id=futsal_id)
    if request.method == 'POST':
        futsal.delete()
        messages.success(request, f' {'Successfully Deleted futsal ' + futsal.name }')
        return redirect('/admin/tables/')  
    return render(request, 'adminHome/delete_futsals.html', {'futsal': futsal})