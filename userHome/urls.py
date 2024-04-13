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
    path('logout/', views.logoutUser, name="logout")
]

