from django.urls import path
from .views import RegisterAPIView,LoginAPIView,UserAPIView,RefreshAPIView,LogoutAPIView,ForgotAPIView,ResetPasswordAPIView,TwoFactorAPIView,SendOTP

urlpatterns = [
    path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('two-factor', TwoFactorAPIView.as_view()),
    path('send-otp', SendOTP.as_view()),
    path('user', UserAPIView.as_view()),
    path('refresh', RefreshAPIView.as_view()),
    path('logout', LogoutAPIView.as_view()),
    path('forgot', ForgotAPIView.as_view()),
    path('reset_password', ResetPasswordAPIView.as_view()),
]
