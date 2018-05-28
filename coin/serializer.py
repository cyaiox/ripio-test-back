from rest_framework.serializers import ModelSerializer
from .models import Coin


class CoinSerializer(ModelSerializer):
    class Meta:
        model = Coin
        fields = ('id', 'name', 'description', 'symbol')
