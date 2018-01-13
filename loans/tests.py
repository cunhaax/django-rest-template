from django.contrib.auth.models import User, Permission
from django.urls import reverse
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.test import APITestCase
from loans.models import Loan, Payment


class LoanTests(APITestCase):
    def setUp(self):
        u = User.objects.create_user(
                'test-user',
                'email@email.com',
                '123QWEasd'
                )
        u.user_permissions.add(Permission.objects.get(codename='change_loan'))
        self.client.force_login(u)

    def test_create_loan(self):
        url = reverse('loans')
        data = {
            'amount': 1000,
            'term': 12,
            'rate': 0.05,
            'date': '2017-08-05 02:18Z'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.count(), 1)
        o = Loan.objects.get()
        self.assertEqual(o.amount, 1000)
        self.assertEqual(o.term, 12)
        self.assertEqual(o.rate, 0.05)
        self.assertEqual(o.date,
                         parse_datetime('2017-08-05 02:18Z'))
        self.assertEqual(response.data,
                         {'loan_id': o.loan_uuid, 'installment': 85.61})


class PaymentTests(APITestCase):
    def setUp(self):
        u = User.objects.create_user(
                'test-user',
                'email@email.com',
                '123QWEasd'
                )
        u.user_permissions.add(
            Permission.objects.get(codename='change_payment'))
        self.client.force_login(u)

        self.loan = Loan.objects.create(amount='1500',
                                        term=24,
                                        rate=0.8,
                                        date='2016-01-01 12:59Z')

    def test_create_payment(self):
        url = reverse('payment', args=[self.loan.loan_uuid])
        data = {
          'payment': 'made',
          'date': '2017-09-05 02:18Z',
          'amount': 85.61,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 1)
        p = Payment.objects.get()
        self.assertEqual(p.payment, Payment.MADE)
        self.assertEqual(p.date,
                         parse_datetime('2017-09-05 02:18Z'))
        self.assertEqual(p.amount, 85.61)
        self.assertEqual(p.loan.loan_uuid, self.loan.loan_uuid)


class BalanceTests(APITestCase):
    def setUp(self):
        u = User.objects.create_user(
                'test-user',
                'email@email.com',
                '123QWEasd'
                )
        u.user_permissions.add(
            Permission.objects.get(codename='change_payment'))
        self.client.force_login(u)

        self.loan = Loan.objects.create(amount='1500',
                                        term=24,
                                        rate=0.8,
                                        date='2016-01-01 12:59Z')

        self.loan = Loan.objects.create(amount='1500',
                                        term=24,
                                        rate=0.08,
                                        date='2016-01-01 12:59Z')
        Payment.objects.create(
                        payment=Payment.MADE,
                        amount=65.14,
                        date=parse_datetime('2017-07-05 02:18Z'),
                        loan=self.loan
        )
        Payment.objects.create(
                        payment=Payment.MISSED,
                        amount=65.14,
                        date=parse_datetime('2017-08-05 10:00Z'),
                        loan=self.loan
        )
        Payment.objects.create(
                        payment=Payment.MADE,
                        amount=65.14,
                        date=parse_datetime('2017-09-05 13:20Z'),
                        loan=self.loan
        )

    def test_balance_all_payments_made(self):
        '''
        TODO: calculate the missed payments
        r = 0.08 / 24.
        installment = [ r + r / ( (1+r) ^ 24 - 1) ] x 1500 = 65.14
        tot dept (2017-10-05) = 65.14 * 24 - (65.14*2) = 1433.08
        '''
        url = reverse('balance', args=[self.loan.loan_uuid])
        data = {
            'date': '2017-10-05 02:18Z'
        }
        response = self.client.post(url, data, format='json')
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data, {'balance': 1433.08})

    def test_balance_some_payments_made(self):
        '''
        TODO: calculate the missed payments
        r = 0.08 / 24.
        installment = [ r + r / ( (1+r) ^ 24 - 1) ] x 1500 = 65.14
        tot dept (2017-08-10) = 65.14 * 24 - 65.14 = 1498.22
        '''
        url = reverse('balance', args=[self.loan.loan_uuid])
        data = {
            'date': '2017-08-10 02:18Z'
        }
        response = self.client.post(url, data, format='json')
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data, {'balance': 1498.22})
