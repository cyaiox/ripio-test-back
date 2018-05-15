from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Transfers, Wallet
from .serializer import TransferSerializer
from .tasks import transfer_money_between_wallets


class TransferView(APIView):
    def get(self, request, wallet=None):
        if wallet:
            try:
                wallet = Wallet.objects.get(pk=wallet)

                transfers = Transfers.objects.filter(
                    Q(from_wallet=wallet) | Q(to_wallet=wallet)
                )

                return Response({
                    "transactions": TransferSerializer(transfers, many=True).data,
                    "balance": wallet.balance
                })
            except:
                return Response({"error": "This is not a valid wallet."})
        
        return Response({"error": "The wallet must be provided."})

    def post(self, request, wallet=None):
        if request.POST or request.data:
            data = request.POST or request.data

            transfer_money_between_wallets.delay(
                data['from_wallet'],
                data['to_wallet'],
                data['amount']
            )

            return Response({"data": "redirecting to balance home page"})
        else:
            return Response({"error": 'NOTHING TO DO HERE :D'})
