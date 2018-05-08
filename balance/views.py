from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import Transfers, Wallet
from .serializer import TransferSerializer


class TransferView(APIView):
    def get(self, request, wallet=None):
        if wallet:
            transfers = Transfers.objects.filter(
                from_wallet=Wallet.objects.get(pk=wallet)
            )
        
            if transfers:        
                return Response(TransferSerializer(transfers, many=True).data)

            return Response({"error": "nothing to see here."})
        
        return Response({"error": "The wallet must be provided."})