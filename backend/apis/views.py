from rest_framework import viewsets

from .models import *
from .serializers import (
    InvestMainSerializer,
    InvestDetailSerializer,
    HoldingSerializer
)

class InvestMainViewSet(viewsets.ModelViewSet):
    """투자 메인 CRUD API"""
    queryset = Account.objects.all()
    serializer_class = InvestMainSerializer


class InvestDetailViewSet(viewsets.ModelViewSet):
    """투자 메인 CRUD API"""
    queryset = Account.objects.all()
    serializer_class = InvestDetailSerializer


class HoldingViewSet(viewsets.ModelViewSet):
    """보유 종목 CRUD API"""
    queryset = User.objects.all()
    serializer_class = HoldingSerializer