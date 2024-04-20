from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('tables/', views.tablePage, name="table"),
    path('bookings/', views.bookingPage, name="bookings"),
    path('addFutsal/', views.addFutsal, name="addFutsal"),
    path('approveBooking/<str:pk>/', views.approveBooking, name="approve_booking"),
    path('rejectBooking/<str:pk>/', views.rejectBooking, name="reject_booking"),
    path('completeBooking/<str:pk>/', views.completeBooking, name="complete_booking"),

    path('manage_user', views.manage_user_view, name="manage_user_view")
]

