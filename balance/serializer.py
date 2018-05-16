from rest_framework.serializers import ModelSerializer
from .models import Transfers, Wallet


class TransferSerializer(ModelSerializer):
    class Meta:
        model = Transfers
        fields = ('id', 'from_wallet', 'to_wallet', 'amount', 
                  'date_time', 'status')


class WalletSerializer(ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('id', 'balance', 'coin')
