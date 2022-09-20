from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import (
    InvestMainSerializer,
    InvestDetailSerializer,
    HoldingSerializer,
    DepositSerializer
)


@api_view(['GET'])
def InvestMainView(request, pk):
    """투자 메인 화면 API"""
    account    = Account.objects.get(id=pk)
    serializer = InvestMainSerializer(account, many=False)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
        )


@api_view(['GET'])
def InvesetDetailView(request, pk):
    """투자 상세 화면 API"""
    account    = Account.objects.get(id=pk)
    serializer = InvestDetailSerializer(account, many=False)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def MyHoldingView(request, pk):
    """보유 종목 화면 API"""
    user         = User.objects.get(id=pk)
    user_holding = UserHolding.objects.filter(user=user)
    serializer   = HoldingSerializer(user_holding, many=True)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def DepositView1(request):
    """투자금 입금 Phase1 API"""
    account    = Account.objects.get(account_number=request.data['account_number'])
    serializer = DepositSerializer(account, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )