from rest_framework_simplejwt.views import TokenRefreshView 
from django.urls import path
from . import views as views

urlpatterns = [
    path("log-in/", views.log_in, name="sign-in or sign-up"),
    path("log-in/confirm/", views.log_in_confirm, name="otp-validation"),
    path("refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
