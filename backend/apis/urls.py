from django.urls import path
from .views import (
    InvestMainView,
    InvesetDetailView,
    MyHoldingView
)


urlpatterns = [
    path('account/<int:pk>/', InvestMainView, name='account'), # 투자 메인 화면,
    path('account-asset/<int:pk>/', InvesetDetailView, name='account-asset'), # 투자 상세 화면,
    path('my-holding/<int:pk>/', MyHoldingView, name='my-holding'), # 보유 종목 화면
]