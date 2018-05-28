from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Wallet, Transfers
from coin.models import Coin
from .views import TransferView


class WalletTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.u1 = User.objects.create(
            username='cyaiox', password=make_password('abcd1234+'))
        self.u2 = User.objects.create(
            username='eli13', password=make_password('abcd1234+'))

        self.c = Coin.objects.create(name='testcoin', symbol='tc')

        self.w1 = Wallet.objects.create(
            user=self.u1, balance=200, coin=self.c)
        self.w2 = Wallet.objects.create(
            user=self.u2, balance=400, coin=self.c)

        response = self.client.post(
            '/auth-token/',
            {"username": self.u1.username, "password": self.u1.password},
            format='json')

    def test_transaction_1(self, amount=100):
        request = self.client.post('/transfers/', {
            "from_wallet": self.w1.id,
            "to_wallet": self.w2.id,
            "amount": amount
        })

        request.user = self.u1

        response = TransferView.as_view()(request)

        print(response)
        self.assertEqual(response.data, {"data": "success"})
