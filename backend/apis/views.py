from rest_framework import viewsets

from .models import *
from .serializers import (
    InvestMainSerializer,
    InvestDetailSerializer
)

class InvestMainViewSet(viewsets.ModelViewSet):
    """투자 메인 CRUD API"""
    queryset = Account.objects.all()
    serializer_class = InvestMainSerializer


class InvestDetailViewSet(viewsets.ModelViewSet):
    """투자 메인 CRUD API"""
    queryset = Account.objects.all()
    serializer_class = InvestDetailSerializer