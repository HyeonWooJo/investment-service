from django.db import models

from users.models import User

class Investment(models.Model):
    company = models.CharField(max_length=40)
    principal = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'investment'

    def __str__(self):
        return self.id