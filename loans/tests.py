from datetime import datetime

from django.urls import reverse
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.test import APITestCase
from loans.models import Loan


class LoanTests(APITestCase):
    def test_create_loan(self):
        """
        Ensure we can create a new loan object.
        """
        url = reverse('loans-list')
        data = {
            'amount': 1000,
            'term': 12,
            'rate': 0.05,
            'date': '2017-08-05 02:18Z'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.count(), 1)
        self.assertEqual(Loan.objects.get().amount, 1000)
        self.assertEqual(Loan.objects.get().term, 12)
        self.assertEqual(Loan.objects.get().rate, 0.05)
        self.assertEqual(Loan.objects.get().date,
                        parse_datetime('2017-08-05 02:18Z'))
        self.assertIsNotNone(Loan.objects.get().loan_uuid)
        self.assertEqual(Loan.objects.get().installment, 85.61)

        print(response.data)
