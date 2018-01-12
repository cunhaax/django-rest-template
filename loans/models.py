import math
import uuid
from django.db import models

class Loan(models.Model):
    amount = models.IntegerField()
    term = models.IntegerField()
    rate = models.FloatField()
    date = models.DateTimeField()
    loan_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    @property
    def installment(self):
        r = self.rate / self.term
        res = (r + r /(math.pow(1+r,self.term)-1)) * self.amount
        return round(res, 2)
