from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from .serializers import UserSerializer
from .models import User,UserToken,ResetPassword
from .authentication import create_access_token,create_refresh_token,JWTAuthentication,decode_refresh_token
import datetime
import random
import string
from django.core.mail import send_mail
import pyotp
from .throttling import OTPSMSRateThrottle
from .sms import SendSMS
import random
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.models import AnonymousUser

class RegisterAPIView(APIView):
    def post(self,request):
        data = request.data
        if data["password"] != data["password_confirm"]:
            raise exceptions.APIException("Password do not mach!")

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class LoginAPIView(APIView):
    def __init__(self):
        # Select Between otp email username
        self.auth_method = "email"
        self.tfa_enabled = False

    def generate_token(self,id):
        access_token = create_access_token(id)
        refresh_token = create_refresh_token(id)
        UserToken.objects.create(user_id = id,token=refresh_token,expired_at = datetime.datetime.utcnow() + datetime.timedelta(days=7))
        response = Response()
        response.set_cookie(key='refresh_token',value=refresh_token,httponly=True)
        response.data = {
            'tfa_status':self.tfa_enabled,
            'token':access_token
        }
        return response
    
    def generate_tfa_secret(self,id):
        secret = pyotp.random_base32()
        otpauth_url = pyotp.totp.TOTP(secret).provisioning_uri(issuer_name = 'Lilinko')
        return Response({
            'tfa_status':self.tfa_enabled,
            'tfa_set':False,
            'id':id,
            'secret':secret,
            'otpauth_url':otpauth_url
        })
    
    def post(self,request):
        if self.auth_method == "email":
            email = request.data["email"]
            password = request.data["password"]
            user = User.objects.filter(email=email).first()
        elif self.auth_method == "username":
            username = request.data["username"]
            password = request.data["password"]
            user = User.objects.filter(username=username).first()
        elif self.auth_method == "otp":
            phone = request.data["phone"]
            code = request.data["code"]
            user = User.objects.filter(phone=phone).first()

        if user is None:
            raise exceptions.AuthenticationFailed('Invalid credentials')
        
        if self.auth_method == "username" or self.auth_method == "email":
            if not user.check_password(password):
                raise exceptions.AuthenticationFailed('Invalid credentials')
            elif not self.tfa_enabled:
                return self.generate_token(user.id)
            else:
                if user.tfa_secret:
                    return Response({
                    'tfa_status':self.tfa_enabled,
                    'tfa_set':True,
                    'id':user.id
                })
                return self.generate_tfa_secret(user.id)
        elif self.auth_method == "otp":
            now = datetime.datetime.now()
            time_dalta = (now - (user.otp_date).replace(tzinfo=None)).total_seconds()
            if time_dalta > 120:
                if user.otp_used:
                    raise exceptions.AuthenticationFailed('Invalid credentials')
                elif check_password(code,user.otp):
                    user.otp_used = True
                    user.save()
                    return self.generate_token(user.id)
                else:
                    raise exceptions.AuthenticationFailed('Invalid credentials')
            else:
                raise exceptions.AuthenticationFailed('Invalid credentials')

            

class SendOTP(APIView):
    throttle_classes = [OTPSMSRateThrottle]
    def post(self,request):
        if isinstance(request.user, AnonymousUser):
            phone = request.data["phone"]
            user = User.objects.filter(phone=phone).first()
            if user is None:
                raise exceptions.AuthenticationFailed('Invalid credentials')
            code = str(random.randint(1000, 9999))
            hashed_code = make_password(code)
            user.otp = hashed_code
            user.otp_used = False
            user.save()
            try:
                sms = SendSMS()
                sms.SendOTP(receptor=user.phone,code=code)
                return Response({"success":True})
            except:
                return Response({"success":False})
        else:
            return Response({"success":False})








class TwoFactorAPIView(APIView):
    def __init__(self):
        self.tfa_enabled = True
    
    def post(self,request):
        id = request.data['id']
        user = User.objects.filter(pk=id).first()
        if not user:
            raise exceptions.AuthenticationFailed('Invalid credentials')
        secret = user.tfa_secret if user.tfa_secret != '' else request.data['secret']
        if not pyotp.TOTP(secret).verify(request.data['code']):
            raise exceptions.AuthenticationFailed('Invalid credentials')
        if user.tfa_secret == '':
            user.tfa_secret = secret
            user.save()
        return LoginAPIView.generate_token(self=self,id=id)

      
class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self,request):
        return Response(UserSerializer(request.user).data)
    
class RefreshAPIView(APIView):
    def post(self,request):
        refresh_token = request.COOKIES.get('refresh_token')
        id = decode_refresh_token(refresh_token)
        if not UserToken.objects.filter(user_id = id , expired_at__gt=datetime.datetime.now(tz=datetime.timezone.utc)).exists():
            raise exceptions.AuthenticationFailed('unathenticated')
        access_token = create_access_token(id)
        return Response({
            'token':access_token
        })
        
class LogoutAPIView(APIView):
    def post(self,request):
        refresh_token = request.COOKIES.get('refresh_token')
        UserToken.objects.filter(token=refresh_token).delete()
        response = Response()
        response.delete_cookie(key='refresh_token')
        response.data = {
            'message':'success'
        }
        return response
    
class ForgotAPIView(APIView):
    def post(self,request):
        email = request.data['email']
        token = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
        ResetPassword.objects.create(email=email,token=token)
        url = f'http://localhost:5000/reset_password/{token}'
        send_mail(subject='Reset your password',message=f'Click <a href="{url}">here</a> to reset password',from_email='from@example.com',recipient_list=[email])
        return Response({'message':'success'})

class ResetPasswordAPIView(APIView):
    def post(self,request):
        data = request.data
        if data["password"] != data["password_confirm"]:
            raise exceptions.APIException("Password do not mach!")
        reset_password = ResetPassword.objects.filter(token=data['token']).first()
        if not reset_password:
            raise exceptions.APIException("Invalid link!")
        user = User.objects.filter(email=reset_password.email).first()
        if not user:
            raise exceptions.APIException("User Not Found")
        user.set_password(data["password"])
        user.save()
        return Response({"message":"success"})
