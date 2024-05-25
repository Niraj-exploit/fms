from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('tables/', views.tablePage, name="table"),
    path('bookings/', views.bookingPage, name="bookings"),
    path('addFutsal/', views.addFutsal, name="addFutsal"),
    path('admin_update_futsal/<int:futsal_id>/', views.update_futsal, name="admin_update_futsal"),
    path('admin_delete_futsal/<int:futsal_id>/', views.delete_futsal, name='admin_delete_futsal'),
    path('approveBooking/<str:pk>/', views.approveBooking, name="approve_booking"),
    path('rejectBooking/<str:pk>/', views.rejectBooking, name="reject_booking"),
    path('completeBooking/<str:pk>/', views.completeBooking, name="complete_booking"),
    path('manage_user', views.manage_user_view, name="manage_user_view"),
    path('update_user/<int:user_id>/', views.update_user, name='update_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('user_detail/<int:user_id>/', views.user_detail, name='user_detail'),

]

