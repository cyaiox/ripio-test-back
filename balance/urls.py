from django.urls import re_path
from balance.views import TransferView

urlpatterns = [
    re_path(r'^((?P<wallet>\w+)/)?$', TransferView.as_view(), name='transfers'),
]
