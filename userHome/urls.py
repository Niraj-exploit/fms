from django.urls import path
from . import views
from adminHome.views import dashboard


urlpatterns = [
    path('dashboard/', views.homePage, name="home"),
    path('admin', dashboard, name="admin"),
    path('my_bookings/', views.myBookings, name="my_bookings"),
    path('futsal_list/', views.futsalPage, name="futsal_list"),
    path('book/<str:pk>/', views.bookFutsal, name="book_futsal"),
    path('initiate_payment/<str:booking_id>/', views.initiate_payment, name="initiate_payment"),
    path('view_bill/<str:booking_id>/', views.view_bill, name="view_bill"),
    path('payment_detail/', views.payment_detail, name='payment_detail'),
    path('cancel/<str:pk>/', views.cancelBooking, name="cancel_booking"),
    path('search/', views.searchFutsal, name='search_futsal'),
    path('manage_futsal/', views.manageFutsal, name="manage_futsal"),
    path('manage_bookings/', views.bookingPage, name="manage_bookings"),
    path('logout/', views.logoutUser, name="logout"),
    path('approveBookingOwn/<str:pk>/', views.approveBooking, name="approve_booking_own"),
    path('rejectBookingOwn/<str:pk>/', views.rejectBooking, name="reject_booking_own"),
    path('completeBookingOwn/<str:pk>/', views.completeBooking, name="complete_booking_own"),
    path('register_team/', views.team_registration, name='team_registration'),
    path('my_team/', views.myTeam, name="my_team"),
    path('find_opponent/', views.find_opponent, name="find_opponent"),
    path('shop/', views.shop_kit, name="shop_kits"),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('add-to-cart/<int:kit_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('manage_kits/', views.manage_kits, name= "manage_kits"),
    path('update-kit/<int:pk>/', views.update_kit, name='update_kit'),
    path('delete-kit/<int:pk>/', views.delete_kit, name='delete_kit'),
]

