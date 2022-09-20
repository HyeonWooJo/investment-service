from django.db import models


class User(models.Model):
    """유저 모델"""
    name = models.CharField(verbose_name="이름", max_length=20)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.name


class Account(models.Model):
    """계좌 모델"""
    account_name   = models.CharField(max_length=40)
    account_number = models.CharField(max_length=45, null=False, unique=True)
    total_assessts = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    user           = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'accounts'

    def __str__(self):
        return self.id

class TransferIdentifier(models.Model):
    """입금 정보 식별자 모델"""
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        db_table = 'transfer_identifiers'

    def __str__(self):
        return self.id


class Investment(models.Model):
    """투자 모델"""
    company   = models.CharField(max_length=40)
    principal = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    account   = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        db_table = 'investment'

    def __str__(self):
        return self.id


class Holding(models.Model):
    """주식 종목 모델"""
    name        = models.CharField(max_length=40, unique=True, null=False, blank=False)
    isin        = models.CharField(max_length=70, unique=True, null=False, blank=False)
    asset_group = models.CharField(max_length=40)

    class Meta:
        db_table = 'holdings'

    def __str__(self):
        return self.id


class UserHolding(models.Model):
    """유저와 주식 종목의 중간 테이블"""
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    holding       = models.ForeignKey(Holding, on_delete=models.CASCADE)
    quantity      = models.PositiveIntegerField(default=0)
    current_price = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    class Meta:
        db_table = 'user_holdings'

    def __str__(self):
        return self.id