from rest_framework import serializers

from .models import *


class InvestMainSerializer(serializers.ModelSerializer):
    """투자 메인 Serializer"""
    company = serializers.SerializerMethodField()

    class Meta:
        model  = Account
        fields = '__all__'

    def get_company(self, object):
        company = object.investment_set.all()[0].company

        return company


class InvestDetailSerializer(serializers.ModelSerializer):
    """투자 상세 Serializer"""
    company        = serializers.SerializerMethodField()
    principal      = serializers.SerializerMethodField()
    total_proceeds = serializers.SerializerMethodField()
    profit_rate    = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = '__all__'

    def get_company(self, object):
        company = object.investment_set.all()[0].company

        return company

    def get_principal(self, object):
        principal = object.investment_set.all()[0].principal

        return principal

    def get_total_proceeds(self, object):
        total_assests = object.total_assessts
        principal     = object.investment_set.all()[0].principal

        return total_assests - principal

    def get_profit_rate(self, object):
        total_assests  = object.total_assessts
        principal      = object.investment_set.all()[0].principal
        total_proceeds = total_assests - principal

        return (total_proceeds / principal * 100)


class HoldingSerializer(serializers.ModelSerializer):
    """보유 종목 Serializer"""
    appraisal_amount = serializers.SerializerMethodField()

    class Meta:
        model = UserHolding
        fields = '__all__'

    def get_appraisal_amount(self, object):
        current_price = object.current_price
        quantity      = object.quantity
        return current_price * quantity


# class DepositSerializer(serializers.ModelSerializer):
