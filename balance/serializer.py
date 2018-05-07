from rest_framework.serializers import ModelSerializer
from .models import Transfers


class TransferSerializer(ModelSerializer):
    class Meta:
        model = Transfers
        fields = ('id', 'from_wallet', 'to_wallet', 'amount', 
                  'date_time', 'status')
