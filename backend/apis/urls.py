from django.urls import path
from .views import (
    InvestMainViewSet,
    InvestDetailViewSet
)

invest_main_list = InvestMainViewSet.as_view({
    'get'  : 'list',
    'post' : 'create'
})
invest_main_detail = InvestMainViewSet.as_view({
    'get' : 'retrieve',
    'put' : 'update',
    'delete' : 'destroy'
})

invest_detail_list = InvestDetailViewSet.as_view({
    'get'  : 'list',
    'post' : 'create'
})
invest_detail_detail = InvestDetailViewSet.as_view({
    'get' : 'retrieve',
    'put' : 'update',
    'delete' : 'destroy'
})

urlpatterns = [
    path('invests/main/', invest_main_list, name='invest-main-list'),
    path('invests/main/<int:pk>/', invest_main_detail, name='invest-main-detail'),
    path('invests/detail/', invest_detail_list, name='invest-detail-list'),
    path('invests/detail/<int:pk>/', invest_detail_detail, name='invest-detail-detail'),
]