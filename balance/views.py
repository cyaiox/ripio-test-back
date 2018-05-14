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

            resp = transfer_money_between_wallets.delay(
                data['from_wallet'],
                data['to_wallet'],
                data['amount']
            )

            return Response({"data": "waiting"})
            # try:
            #     from_wallet = Wallet.objects.get(pk=data['from_wallet'])
            #     to_wallet = Wallet.objects.get(pk=data['to_wallet'])
            #
            #     if from_wallet.balance - (data['amount'] + from_wallet.escrow) >= 0:
            #         Transfers(from_wallet=from_wallet,
            #                   to_wallet=to_wallet,
            #                   amount=data['amount'],
            #                   status='A').save()
            #
            #         from_wallet.balance -= data['amount']
            #         from_wallet.save()
            #
            #         to_wallet.balance += data['amount']
            #         to_wallet.save()
            #
            #         return Response({"data": "success"})
            #     else:
            #         return Response({"error": "404 NOT FUNDS FOUND"})
            # except:
            #     return Response({"error": "ALIENS!"})
        else:
            return Response({"error": 'NOTHING TO DO HERE :D'})
