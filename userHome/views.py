from django import template
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from adminHome.models import BookingStatus, Futsal, OpponentStatus
from django.contrib.auth import logout
from adminHome.models import Futsal, Booking
from userAuth.models import User
from django.contrib import messages

from userHome.models import Player, Team, FutsalKit, CartItem
from .forms import FutsalSearchForm, TeamForm, PlayerForm, FutsalKitForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from adminHome.forms import AddFutsalForm
from django.shortcuts import render, redirect
from django.conf import settings
import requests
import json
from adminHome.utils import find_most_booked_futsal_for_week
from .utils import find_nearest_booking

@login_required
def homePage(request):
    futsals = Futsal.objects.all()
    total_futsals = Futsal.objects.count()
    form = FutsalSearchForm()
    futsal_types = Futsal.objects.values_list('futsal_type', flat=True).distinct()
    nearest_booking = find_nearest_booking(request.user)
    most_booked_futsal, num_bookings = find_most_booked_futsal_for_week()
    print("Nearest booking time", nearest_booking)

    if request.user.is_authenticated:
        user_booked_futsals = Booking.objects.filter(user=request.user)
        user_booked_count = Booking.objects.filter(user=request.user).count()
        user_team = getattr(request.user, 'user_team', None)
    else:
        user_booked_futsals = None
        user_team = None

    context = {
        'futsals': futsals,
        'total_futsals': total_futsals,
        'futsal_types': futsal_types,
        'user_booked_futsals': user_booked_futsals,
        'user_booked_count': user_booked_count,
        'most_booked_futsal': most_booked_futsal,
        'form': form,
        'nearest_booking': nearest_booking,
        'user_team': user_team,
    }

    return render(request, 'userHome/home.html', context)


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

@login_required
def bookFutsal(request, pk):
    futsal = Futsal.objects.get(id=pk)
    user = request.user
    user_team = Team.objects.filter(name=user.user_team).first()
    if user_team:
        location_parts = user_team.team_location.split(',')
        location_parts = [part.strip() for part in location_parts]
        # Build the query to find teams with matching location parts
        query = Q()
        for part in location_parts:
            query |= Q(team_location__icontains=part)
        
        # Search for nearby teams based on the constructed query
        nearby_teams = Team.objects.filter(query).exclude(id=user_team.id)


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
        # opponent_id = request.POST.get('opponent_id')
        # opponent = Team.objects.get(id=opponent_id)
        try:
            booking = Booking.objects.create(
            user=request.user,
            futsal=Futsal.objects.get(id=pk),
            booking_date=booking_date,
            booking_time=booking_time,
            book_time=book_time,
            total_price=total_price,
            # opponent=opponent 
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
        'nearest_teams': nearby_teams,
        'team_location': user_team.team_location,

    }
    return render(request, 'userHome/checkout.html', context)



def futsal_section(request):
    futsals = Futsal.objects.all()

@login_required
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required
def myBookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-id')
    user_team_logo_url = request.user.user_team.logo.url if request.user.user_team else None
    
    booking_opponent_data = []
    for booking in bookings:
        opponent_logo_url = booking.opponent.logo.url if booking.opponent else None
        booking_opponent_data.append((booking, opponent_logo_url))

    context = {
        'booking_opponent_data': booking_opponent_data,
        'user_team_logo_url': user_team_logo_url,
    }
    return render(request, 'userHome/my_bookings.html', context)



def topBooked(request):
    topBooked = Booking.object.filter()

@login_required
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

@login_required
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

@login_required
def cancelBooking(request, pk):
    booking = Booking.objects.get(id=pk)
    try:
        booking.delete()
        messages.success(request, f'Booking Cancelled')
    except Exception as e:
        raise Exception("Booking Cancellation Failed" + str(e))
    
    return redirect('my_bookings')

@login_required
def manageFutsal(request):
    futsals = Futsal.objects.filter(addedBy=request.user)
    futsal_form = AddFutsalForm()

    if request.method == 'POST':
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
def update_futsal(request, futsal_id):
    futsal = get_object_or_404(Futsal, pk=futsal_id, addedBy=request.user)
    if request.method == 'POST':
        form = AddFutsalForm(request.POST, instance=futsal)
        if form.is_valid():
            form.save()
            return redirect('manage_futsal')
    else:
        form = AddFutsalForm(instance=futsal)
    return render(request, 'userHome/update_owned_futsal.html', {'form': form})

@login_required
def delete_futsal(request, futsal_id):
    futsal = get_object_or_404(Futsal, id=futsal_id)
    if request.method == 'POST':
        futsal.delete()
        messages.success(request, f' {'Successfully Deleted futsal ' + futsal.name }')
        return redirect('/manage_futsal/')  
    return render(request, 'userHome/delete_futsals.html', {'futsal': futsal})

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
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        response_data = json.loads(response.text)
        payment_url = response_data.get('payment_url')
        return redirect(payment_url)
    except requests.RequestException as e:
        # Handle request exception
        return render(request, 'payment_error.html', {'error_message': str(e)})

@login_required
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

@login_required
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

@login_required
def bookingPage(request): 
    owner_id = request.user.id
    bookings = Booking.objects.filter(futsal__addedBy_id=owner_id)

    context = {
        'bookings': bookings,
    }
    return render(request, 'userHome/manage_own_booking.html', context)


def approveBooking(request, pk):
    booking = Booking.objects.get(id=pk)
    booking.status = 'Approved'
    booking.save()
    return redirect('/manage_bookings/')

def rejectBooking(request, pk):
    booking = Booking.objects.get(id=pk)
    booking.status = 'Rejected'
    booking.save()
    return redirect('/manage_bookings/')

def completeBooking(request, pk):
    booking = Booking.objects.get(id=pk)
    booking.status = 'Completed'
    booking.save()
    return redirect('/manage_bookings/')

@login_required
def myTeam(request): 
    user = request.user
    print("User avatar",user.avatar.url)
    if user.is_authenticated and user.user_team:
        team = user.user_team
        team_detail = Team.objects.filter(name=team.name).first()  
        print(team_detail)
        player_detail = Player.objects.filter(team = team_detail.id)
        print(player_detail)
        player_form = PlayerForm()
        if request.method == 'POST':
            player_form = PlayerForm(request.POST, request.FILES)
            if player_form.is_valid():
                new_player = player_form.save(commit=False)
                new_player.team = team_detail
                new_player.save()

        if player_detail:  
            context = {
                'team': team_detail,
                'team_exists': True,
                'player_exists': True,
                'players': player_detail,
                'player_form': player_form
            }
            return render(request, 'userHome/my_team.html', context)
        else:
            context = {
                'team': team_detail,
                'team_exists': True,
                'player_exists': False
            }
            return render(request, 'userHome/my_team.html', context)
    else:
        return render(request, 'userHome/my_team.html', {'team_exists': False})



def team_registration(request):
    if request.method == 'POST':
        team_form = TeamForm(request.POST, request.FILES)
        if team_form.is_valid():
            team = team_form.save()  # Save the team first

            user = request.user
            user.user_team = team  # Update user's team
            user.save()

            player = Player.objects.create(
                team=team,
                name=user.username,
                role='Captain',
                image=user.avatar.url,
                player_location=user.address
            )

            team.captain = player  # Set the team's captain
            team.save()  # Save the team again to update captain

            return redirect('my_team')
    else:
        team_form = TeamForm()
    return render(request, 'userHome/team_registration.html', {'team_form': team_form})

def destroy_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    
    Booking.objects.filter(opponent=team).delete()
    
    Player.objects.filter(team=team).delete()
    
    team.delete()
    
    messages.success(request, 'Team and its associated bookings and players have been successfully deleted.')
    return redirect('/my_team/')

def find_opponent(request):
    user = request.user
    user_team = Team.objects.filter(name=user.user_team).first()
    
    if user_team:
        # Split the user's team location into individual words
        location_parts = user_team.team_location.split(',')
        location_parts = [part.strip() for part in location_parts]

        # Build the query to find teams with matching location parts
        query = Q()
        for part in location_parts:
            query |= Q(team_location__icontains=part)
        
        # Search for nearby teams based on the constructed query
        nearby_teams = Team.objects.filter(query).exclude(id=user_team.id)

        # Get all teams excluding the user's team
        all_teams = Team.objects.all().exclude(id=user_team.id)

        context = {
            'nearest_teams': nearby_teams,
            'team_location': user_team.team_location,
            'teams': all_teams
        }
    else:
        context = {
            'teams': []
        }

    return render(request, 'userHome/find_opponent.html', context)

def shop_kit(request):
    available_kits = FutsalKit.objects.all()
    context = {
        'available_kits': available_kits
    }
    return render(request, 'userHome/shop_kit.html', context)

@login_required
def add_to_cart(request, kit_id):
    kit = get_object_or_404(FutsalKit, id=kit_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, kit=kit)
    if not created:
        cart_item.quantity += 1
    cart_item.total_price = cart_item.quantity * kit.price
    cart_item.save()
    return redirect('shop_kits')


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    context = {
        'cart_items': cart_items
    }
    return render(request, 'userHome/cart.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(CartItem, id=order_id, user=request.user)

    context = {
        'order': order
    }
    return render(request, 'userHome/order_detail.html', context)

def remove_from_cart(request, order_id):
    order = get_object_or_404(CartItem, id=order_id, user=request.user)
    order.delete()
    return redirect("/cart/")

register = template.Library()

@register.filter
def progress_percentage(status):
    if status == 'Pending':
        return 50
    elif status == 'Success':
        return 100
    return 0

@register.filter
def status_class(status):
    if status == 'Pending':
        return 'bg-warning'
    elif status == 'Success':
        return 'bg-success'
    return 'bg-secondary'

@login_required
def manage_kits(request):
    user = request.user
    kit_form = FutsalKitForm(user=request.user)

    if user.is_futsal_owner:
        futsalKits = FutsalKit.objects.filter(added_by=user)
    else:
        futsalKits = []

    if request.method == 'POST':
        kit_form = FutsalKitForm(request.POST, request.FILES, user=request.user)
        if kit_form.is_valid():
            new_kit = kit_form.save(commit=False)
            new_kit.added_by = user
            new_kit.save()
            return redirect('manage_kits')

    context = {
        'futsalKits': futsalKits,
        'kit_form': kit_form
    }
    return render(request, 'userHome/owner_futsal_kit.html', context)

@login_required
def update_kit(request, pk):
    kit = get_object_or_404(FutsalKit, pk=pk, added_by=request.user)
    if request.method == 'POST':
        form = FutsalKitForm(request.POST, request.FILES, instance=kit, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('manage_kits')
    else:
        form = FutsalKitForm(instance=kit, user=request.user)
    return render(request, 'userHome/update_futsal_kit.html', {'form': form, 'kit': kit})

@login_required
def delete_kit(request, pk):
    kit = get_object_or_404(FutsalKit, pk=pk, added_by=request.user)
    if request.method == 'POST':
        kit.delete()
        return redirect('manage_kits')
    return render(request, 'userHome/delete_futsal_kit.html', {'kit': kit})


@login_required
def order_initiate_payment(request, order_id):
    order = get_object_or_404(CartItem, id=order_id, user=request.user)
    order_price = float(order.total_price) * 100
    print(order_price)

    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    payload = json.dumps({
        "return_url": "http://localhost:8000/order_payment_detail/",
        "website_url": "https://example.com/",
        "amount": str(order_price),
        "purchase_order_id": str(order_id),
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
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        response_data = json.loads(response.text)
        payment_url = response_data.get('payment_url')
        return redirect(payment_url)
    except requests.RequestException as e:
        # Handle request exception
        return render(request, 'payment_error.html', {'error_message': str(e)})
    
@login_required
def order_payment_detail(request):
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
        cart_instance = CartItem.objects.get(id=purchase_order_id)
    except CartItem.DoesNotExist:
        return HttpResponse("CartItem not found", status=404)

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
        cart_instance.payment_status = 'Completed'
        cart_instance.pidx = response_data.get('pidx')
        cart_instance.save()

        kit_instance = cart_instance.kit
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
            'cartItem':cart_instance,
            'kit': kit_instance
        }
        return render(request, 'userHome/order_item_bill.html', context)
    else:
        print("Payment not completed")
        return HttpResponse("Payment not completed", status=400)

@login_required
def order_view_bill(request, order_id):
    try:
        cart_instance = CartItem.objects.get(id=order_id)
    except CartItem.DoesNotExist:
        return HttpResponse("CartItem not found", status=404)

    pidx = cart_instance.pidx
    kit_instance = cart_instance.kit

    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    payload = json.dumps({"pidx": pidx})
    headers = {
        'Authorization': 'key live_secret_key_68791341fdd94846a146f0457ff7b455',
        'Content-Type': 'application/json',
    }

    response = requests.post(url, headers=headers, data=payload)
    response_data = response.json()
    print("Response: ", response_data)

    mobile = request.user.phone
    total_amount = response_data.get('total_amount') / 100
    tidx = 'sdasda'

    context = {
        'pidx': response_data.get('pidx'),
        'transaction_id': response_data.get('transaction_id'),
        'tidx': tidx,
        'total_amount': total_amount,
        'mobile': mobile,
        'status': response_data.get('status'),
        'fee': response_data.get('fee'),
        'refunded': response_data.get('refunded'),
        'cartItem': cart_instance,
        'kit': kit_instance,
    }

    return render(request, 'userHome/order_item_bill.html', context)

@login_required
def booking_page(request, team_id):
    futsals = Futsal.objects.all()
    opponent_team = get_object_or_404(Team, id=team_id)
    context = {
        "futsals": futsals,
        "opponent_team": opponent_team
    }
    return render(request, 'userHome/get_futsals.html', context)


@login_required
def book_futsal_with_opponent(request, futsal_id, team_id):
    futsal = get_object_or_404(Futsal, id=futsal_id)
    opponent_team = get_object_or_404(Team, id=team_id)
    opponent_captain = opponent_team.captain.name
    
    if request.method == "POST":
        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')
        book_time = request.POST.get('book_time')

        user_booking = Booking(
            user=request.user,
            futsal=futsal,
            booking_date=booking_date,
            booking_time=booking_time,
            book_time=book_time,
            opponent=opponent_team,
            total_price=futsal.price * int(book_time)
        )
        user_booking.save()

        return redirect('/my_bookings/')  # Update this to the correct URL

    context = {
        'futsal': futsal,
        'opponent': opponent_team,
    }
    return render(request, 'userHome/book_futsal_with_opponent.html', context)

@login_required
def opponent_booked_futsals(request):
    # Get the user's team and its details
    user_team = request.user.user_team
    user_team_detail = Team.objects.filter(name=user_team).first()
    user_team_logo_url = user_team_detail.logo.url if user_team_detail and user_team_detail.logo else None

    # Get bookings where the opponent is the user's team
    bookings = Booking.objects.filter(opponent=user_team).order_by('-id')

    # Prepare data for rendering
    booking_opponent_data = []
    for booking in bookings:
        opponent_logo_url = booking.user.user_team.logo.url if booking.user.user_team and booking.user.user_team.logo else None
        booking_opponent_data.append((booking, opponent_logo_url))

    context = {
        'booking_opponent_data': booking_opponent_data,
        'user_team_logo_url': user_team_logo_url,
    }
    return render(request, 'userHome/opponent_booked_futsals.html', context)

@login_required
def accept_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.opponent_status = OpponentStatus.APPROVED.value
    booking.save()
    return redirect('opponent_booked_futsals')

@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.opponent_status = OpponentStatus.REJECTED.value
    booking.save()
    return redirect('opponent_booked_futsals')