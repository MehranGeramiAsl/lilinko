from .kavenegar import KavenegarAPI,APIException,HTTPException
from django.conf import settings

class SendSMS:
    def __init__(self):
        self.token = settings.KAVENEGAR_TOKEN
    def SendOTP(self,receptor,code):
        try:
            api = KavenegarAPI(self.token, timeout=20)
            params = {
                'receptor': receptor,
                'template': 'hinza-report-send-code-to-company',
                'token': code,
                'type': 'sms',#sms or call
            }   
            response = api.verify_lookup(params)
            print(response)
        except APIException as e: 
            print(e)
        except HTTPException as e: 
            print(e)

