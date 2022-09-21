from django.urls import path
from .views import (
    InvestMainView,
    InvesetDetailView,
    MyHoldingView,
    DepositValidationView,
    DepositView
)


urlpatterns = [
    path('account/<int:pk>/', InvestMainView, name='account'), # 투자 메인 화면 API,
    path('account-asset/<int:pk>/', InvesetDetailView, name='account-asset'), # 투자 상세 화면 API,
    path('my-holding/<int:pk>/', MyHoldingView, name='my-holding'), # 보유 종목 화면 API,
    path('deposit-validation/', DepositValidationView, name='deposit-validation'), # 투자금 입금 유효성 검사 API,
    path('deposit/', DepositView, name='deposit'), # 투자금 입금 API,
]