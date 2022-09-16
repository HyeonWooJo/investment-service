from django.db import models


class User(models.Model):
    """유저 모델"""
    name = models.CharField(verbose_name="이름", max_length=20)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.name