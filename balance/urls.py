from django.urls import path, re_path
from .views import TransferView, WalletView

urlpatterns = [
    re_path(r'^transfers/(?P<wallet>\w+)/$', TransferView.as_view(), name='transfers'),
    path('wallets/', WalletView.as_view(), name='wallets')
]
