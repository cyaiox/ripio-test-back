from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Transfers, Wallet
from .serializer import TransferSerializer


class TransferView(APIView):
    def get(self, request, wallet=None):
        if wallet:
            wallet = Wallet.objects.get(pk=wallet)

            transfers = Transfers.objects.filter(
                Q(from_wallet=wallet) | Q(to_wallet=wallet)
            )
        
            if transfers:
                balance = 0
                for transfer in transfers:
                    balance += transfer.amount if transfer.to_wallet_id == wallet.pk else (transfer.amount * -1)

                return Response({
                    "transactions": TransferSerializer(transfers, many=True).data,
                    "balance": balance
                })

            return Response({"error": "nothing to see here."})
        
        return Response({"error": "The wallet must be provided."})

    def post(self, request, wallet=None):
        if request.POST or request.data:
            data = request.POST or request.data

            try:
                from_wallet = Wallet.objects.get(pk=data['from_wallet'])
                to_wallet = Wallet.objects.get(pk=data['to_wallet'])

                if from_wallet.balance - (data['amount'] + from_wallet.escrow) >= 0:
                    Transfers(from_wallet=from_wallet,
                              to_wallet=to_wallet,
                              amount=data['amount']).save()

                    from_wallet.balance -= data['amount']
                    from_wallet.save()

                    to_wallet.balance += data['amount']
                    to_wallet.save()

                    return Response({"data": "success"})
                else:
                    return Response({"error": "404 NOT FUNDS FOUND"})
            except:
                return Response({"error": "ALIENS!"})
        else:
            return Response({"error": 'NOTHING TO DO HERE :D'})
