import math
import uuid
from django.db import models
from django.db.models import Sum


class Loan(models.Model):
    # TODO: Maybe the max value of the integer for the 'amount' is not
    # enough for a very big bank...
    # Do field validation (eg enforce positive numbers)

    # loan amount in dollars
    amount = models.FloatField()
    # number of months that will take until its gets paid-off
    term = models.IntegerField()
    # interest rate as decimal
    rate = models.FloatField()
    # when a loan was asked
    date = models.DateTimeField()
    loan_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    @property
    def installment(self):
        '''
        calculated value for monthly loan payment
        r = rate / 12.
        Installment (monthly) = [ r + r / ( (1+r) ^ term - 1) ] x amount
        '''
        # TODO: the rounding of this value might not be exaclty how banks do it

        r = self.rate / self.term
        res = (r + r / (math.pow(1+r, self.term)-1)) * self.amount
        return round(res, 2)


class PaymentManager(models.Manager):
    def paid_sum(self, loan_uuid, date):
        p = self.filter(loan__loan_uuid=loan_uuid,
                        payment=Payment.MADE,
                        date__lte=date) \
                .aggregate(paid_sum=Sum('amount'))
        res = p.get('paid_sum')
        if not res:
            return 0
        else:
            return res


class Payment(models.Model):
    MADE = 'made'
    MISSED = 'missed'
    STATUS = ((MADE, 'made'), (MISSED, 'missed'))

    payment = models.TextField(choices=STATUS)
    amount = models.FloatField()
    date = models.DateTimeField()

    loan = models.ForeignKey(Loan, models.CASCADE)

    objects = PaymentManager()


class Balance:
    def __init__(self, loan_uuid):
        self._loan_uuid = loan_uuid

    def calculate(self, date):
        loan = Loan.objects.get(loan_uuid=self._loan_uuid)
        total_dept = loan.installment * loan.term

        balance = total_dept - \
            Payment.objects.paid_sum(self._loan_uuid, date)
        # TODO: need to calculate and add the missed payments
        # probably there's a formula for that (adding some interest rate)
        return round(balance, 2)
