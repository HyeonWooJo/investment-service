from rest_framework import viewsets

from .models import *
from .serializers import (
    AccountSerializer
)

class MainViewSet(viewsets.ModelViewSet):
    """메인화면 CRUD API"""
    queryset = Account.objects.all()
    serializer_class = AccountSerializer