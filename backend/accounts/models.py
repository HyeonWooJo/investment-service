from django.db import models

from users.models import User

class Account(models.Model):
    """계좌 모델"""
    account_name = models.CharField(max_length=40)
    account_number = models.PositiveIntegerField()
    total_assessts = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'accounts'

    def __str__(self):
        return self.id