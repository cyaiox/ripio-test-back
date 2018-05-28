from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
#from rest_framework.views import APIView
from django.conf import settings
from datetime import datetime, timedelta
import pytz
from profiles.serializer import UserSerializer


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


class IsAdminUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff


#class UserCreate(APIView):
#    def post(self, request, format='json'):
#        data = request.data or request.post
#        serializer = UserSerializer(data=data)
#        if serializer.is_valid():
#            user = serializer.save()
#            if user:
#                token = Token.objects.create(user=user)
#                return Response({
#                    'token': token.key,
#                    'user': serializer.data
#                }, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

