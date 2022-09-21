from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.db import transaction

from .models import *
from .hash import hash_info


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
        model  = Account
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
        model  = UserHolding
        fields = '__all__'

    def get_appraisal_amount(self, object):
        current_price = object.current_price
        quantity      = object.quantity
        return current_price * quantity


class DepositValidationSerializer(serializers.ModelSerializer):
    """투자금 입금 유효성 검사 Serializer"""
    transfer_identifier = serializers.ReadOnlyField(source="id")

    class Meta:
        model   = TransferIdentifier
        fields  = [
            'transfer_identifier',
            'account_number',
            'user_name',
            'transfer_amount'
            ]
        extra_kwargs = {
            "user_name": {"write_only": True},
            "account_number": {"write_only": True},
            "transfer_amount": {"write_only": True},
        }

    def create(self, validated_data):
        account = Account.objects.get(account_number=validated_data['account_number'])
        transfer_identifier = TransferIdentifier.objects.create(
            account = account,
            status  = 'validated',
            **validated_data
        )
        return transfer_identifier


    def validate(self, data):
        """유저와 계좌에 대한 유효성 검사"""
        user         = User.objects.get(name=data.get('user_name'))
        account_user = Account.objects.get(account_number=data.get('account_number')).user
        if user != account_user:
            raise ValidationError('유저와 계좌의 유저가 다릅니다.')
        return data


class DepositSerialzer(serializers.ModelSerializer):
    """투자금 입금 Serializer"""
    transfer_identifier = serializers.CharField(max_length=50, write_only=True)
    signature = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model   = TransferIdentifier
        fields  = [
            'transfer_identifier',
            'signature',
            'status'
            ]

    def validate(self, data):
        signature           = data['signature']
        transfer_identifier = data['transfer_identifier']
        transfer = TransferIdentifier.objects.get(
            id=transfer_identifier
            )
        transfer_info_str = f'{transfer.account_number}{transfer.user_name}{transfer.transfer_amount}'
        transfer_hash     = hash_info(transfer_info_str)

        """시그니처 유효성 검사"""
        if signature != transfer_hash:
            raise ValidationError('시그니처의 값이 유효하지 않습니다.')
        return data

    @transaction.atomic
    def update(self, instance, validated_data):
        try: 
            """이미 완료된 입금 프로세스 유효성 검사"""
            if instance.status == 'true':
                raise ValidationError('이미 입금 완료된 작업입니다.')

            """유효성 검사 통과 및 status를 true로 수정"""
            instance.status = 'true'
            instance.save()
            
            """식별자에 연결된 계좌에 투자금 입금"""
            account = Account.objects.get(
                account_number = instance.account_number
            )
            account.total_assessts += instance.transfer_amount
            account.save()
            
            return instance
            
        except Exception as e:
            transaction.set_rollback(rollback=True)
            raise ValidationError(str(e))