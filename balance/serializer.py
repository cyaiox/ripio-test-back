from rest_framework.serializers import ModelSerializer
from .models import Transfers, Wallet
from coin.serializer import CoinSerializer


class TransferSerializer(ModelSerializer):
    class Meta:
        model = Transfers
        fields = ('id', 'from_wallet', 'to_wallet', 'amount', 
                  'date_time', 'status')


class WalletSerializer(ModelSerializer):
    coin = CoinSerializer(read_only=True)

    class Meta:
        model = Wallet
        fields = ('id', 'balance', 'coin')
