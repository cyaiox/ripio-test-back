from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from datetime import datetime, timedelta
import pytz


AUTH_TTL = getattr(settings, 'AUTH_TTL', 15)


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted')

        # This is required for the time comparison
        utc_now = datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if token.created < utc_now - timedelta(minutes=AUTH_TTL):
            raise AuthenticationFailed('Token has expired')
        else:
            token.created = utc_now
            token.save()

        return token.user, token

