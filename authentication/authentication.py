import jwt,datetime
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication,get_authorization_header
from .models import User
from .views import UserSerializer
from django.conf import settings

class JWTAuthentication(BaseAuthentication):
    def authenticate(self,request):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)
            user = User.objects.get(pk=id)
            return (user,None)
        raise exceptions.AuthenticationFailed('unauthenticated')

def create_access_token(id):
    return jwt.encode({
        'user_id':id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
        'iat':  datetime.datetime.utcnow()
    },settings.ACCESS_TOKEN_SECRET,algorithm='HS256')
    
def decode_access_token(token):
    try:
        payload = jwt.decode(token,settings.ACCESS_TOKEN_SECRET,algorithms='HS256')
        return payload['user_id']
    except:
        raise exceptions.AuthenticationFailed('unathenticated')
        
    
def create_refresh_token(id):
    return jwt.encode({
        'user_id':id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat':  datetime.datetime.utcnow()
    },settings.REFRESH_TOKEN_SECRET,algorithm='HS256')
    
def decode_refresh_token(token):
    try:
        payload = jwt.decode(token,settings.REFRESH_TOKEN_SECRET,algorithms='HS256')
        return payload['user_id']
    except Exception as e:
        print(e)
        raise exceptions.AuthenticationFailed('unathenticated')