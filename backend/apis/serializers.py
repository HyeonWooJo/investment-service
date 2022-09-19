from rest_framework import serializers

from .models import *


class InvestMainSerializer(serializers.ModelSerializer):
    """투자 메인 Serializer"""
    company = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = '__all__'

    def get_company(self, object):
        company = object.user.invesetmet_set.company

        return company


class InvestDetailSerializer(serializers.ModelSerializer):
    """투자 상세 Serializer"""
    company = serializers.SerializerMethodField()
    principal = serializers.SerializerMethodField()
    total_proceeds = serializers.SerializerMethodField()
    profit_rate = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = '__all__'

    def get_company(self, object):
        company = object.user.invesetmet_set.company

        return company

    def get_principal(self, object):
        principal = object.user.invesetmet_set.principal

        return principal

    def get_total_proceeds(self, object):
        total_assests = object.total_assessts
        principal = object.user.invesetmet_set.principal

        return total_assests - principal

    def get_profit_rate(self, object):
        total_assests = object.total_assessts
        principal = object.user.invesetmet_set.principal
        total_proceeds = total_assests - principal

        return (total_proceeds / principal * 100)


class HoldingSerializer(serializers.ModelSerializer):
    """보유 종목 Serializer"""
    holding_name = serializers.SerializerMethodField()
    asset_group = serializers.SerializerMethodField()
    isin = serializers.SerializerMethodField()
    appraisal_amount = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = '__all__'

    def get_holding_name(self, object):
        return object.userholding_set.holding.name
    
    def get_asset_group(self, object):
        return object.userholding_set.holding.asset_group

    def get_isin(self, object):
        return object.userholding_set.holding.isin

    def get_appraisal_amount(self, object):
        current_price = object.userholding_set.holding.current_price
        quantity = object.userholding_set.quantity

        return current_price * quantity