from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import (
    InvestMainSerializer,
    InvestDetailSerializer,
    HoldingSerializer
)


@api_view(['GET'])
def InvestMainView(request, pk):
    """투자 메인 화면"""
    account = Account.objects.get(id=pk)
    serializer = InvestMainSerializer(account, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def InvesetDetailView(request, pk):
    """투자 상세 화면"""
    account = Account.objects.get(id=pk)
    serializer = InvestDetailSerializer(account, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def MyHoldingView(request, pk):
    """보유 종목 CRUD API"""
    user = User.objects.get(id=pk)
    user_holding = UserHolding.objects.filter(user=user)
    serializer = HoldingSerializer(user_holding, many=True)
    return Response(serializer.data)