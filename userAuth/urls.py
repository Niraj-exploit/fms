from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingPage, name="landing"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('owner_register/', views.ownerRegisterPage, name="owner_register"),
]