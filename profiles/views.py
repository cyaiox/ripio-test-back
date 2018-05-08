from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializer import UserSerializer
from datetime import datetime, timedelta
import pytz


class AuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            utc_now = datetime.utcnow()
            utc_now = utc_now.replace(tzinfo=pytz.utc)

            if not created and token.created < utc_now - timedelta(minutes=15):
                token.delete()
                token = Token.objects.create(user=user)
                token.created = utc_now
                token.save()

            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
