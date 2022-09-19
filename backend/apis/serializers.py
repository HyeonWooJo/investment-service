from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import *


class AccountSerializer(serializers.ModelSerializer):
    """상품 이미지 Serializer"""

    class Meta:
        model = Account
        fields = '__all__'

    def get_company(self, object):
        company = object.user.invesetmet_set.company

        return company