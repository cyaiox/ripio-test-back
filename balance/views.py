from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Transfers, Wallet
from coin.models import Coin
from .serializer import TransferSerializer, WalletSerializer
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


class WalletView(APIView):

    def get(self, request):
        try:
            wallets = Wallet.objects.filter(user=request.user)

            return Response({"data": WalletSerializer(wallets, many=True).data})
        except:
            return Response({"error": "404 WALLETS NOT FOUND"})

    def post(self, request):
        try:
            if request.POST or request.data:
                data = request.POST or request.data

                wallet = Wallet(user=request.user,
                                coin=Coin.objects.get(pk=data['coin']))

                wallet.save()

                return Response({"data": WalletSerializer(wallet).data})
        except:
            return Response({"error": "500 WRONG WAY"})