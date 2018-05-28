from altcoin.authentication import IsAdminUserOrReadOnly
from rest_framework.viewsets import ModelViewSet
from .models import Coin
from .serializer import CoinSerializer


class CoinViewSet(ModelViewSet):
    queryset = Coin.objects.filter(approved=True)
    serializer_class = CoinSerializer
    permission_classes = [IsAdminUserOrReadOnly]
