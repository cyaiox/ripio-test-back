from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import Transfers, Wallet
from .serializer import TransferSerializer


class TransferView(APIView):
    def get(self, request, pk='zmjqgF'):
        transfers = Transfers.objects.filter(
            from_wallet=Wallet.objects.get(pk=pk)
        )
        
        if transfers:        
            return Response(TransferSerializer(transfers))

        return Response({"error": "nothing to see here"})