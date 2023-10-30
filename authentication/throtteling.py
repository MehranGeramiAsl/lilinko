from rest_framework.throttling import UserRateThrottle,AnonRateThrottle


class OTPSMSRateThrottle(AnonRateThrottle):
    rate = '1/s'
    def parse_rate(self, rate):
        return (1, 120) # 1 SMS Per 120 Second

