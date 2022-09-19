from django.urls import path
from .views import (
    MainViewSet
)

main_list = MainViewSet.as_view({
    'get'  : 'list',
    'post' : 'create'
})
main_detail = MainViewSet.as_view({
    'get' : 'retrieve',
    'put' : 'update',
    'delete' : 'destroy'
})

urlpatterns = [
    path('main/', main_list, name='main-list'),
    path('main/<int:pk>/', main_detail, name='main-detail'),
]