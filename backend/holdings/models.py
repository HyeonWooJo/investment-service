from django.db import models

from users.models import User

class Holding(models.Model):
    """주식 종목 모델"""
    name = models.CharField(max_length=40)
    isin = models.CharField(max_length=70)
    current_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    asset_group = models.CharField(max_length=40)

    class Meta:
        db_table = 'holdings'

    def __str__(self):
        return self.id


class UserHolding(models.Model):
    """유저와 주식 종목의 중간 테이블"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    holding = models.ForeignKey(Holding, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'user_holdings'

    def __str__(self):
        return self.id