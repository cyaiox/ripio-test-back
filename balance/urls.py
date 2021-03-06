from django.urls import path, re_path
from .views import TransferView, WalletsView, WalletView

urlpatterns = [
    re_path(r'^transfers/(?P<wallet>\w+)/$', TransferView.as_view(), name='transfers'),
    path('wallets/', WalletsView.as_view(), name='wallets'),
    re_path(r'^wallet/((?P<wallet>\w+)/)?$', WalletView.as_view(), name='wallet')
]
