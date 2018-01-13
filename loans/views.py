from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Balance, Loan, Payment
from .serializers import LoanSerializer, PaymentSerializer


@api_view(['GET', 'POST'])
@permission_required('loans.change_loan', 'api-auth/login')
def loans(request):
    # TODO: results pagination for GET
    if request.method == 'GET':
        loans = Loan.objects.all()
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = {'loan_id': serializer.instance.loan_uuid,
                   'installment': serializer.instance.installment}
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@login_required(login_url='api-auth/login')
def detail(request, loan_id):
    if request.method == 'GET':
        loan = get_object_or_404(Loan, loan_uuid=loan_id)
        return Response(LoanSerializer(loan).data)


@api_view(['GET', 'POST'])
@permission_required('loans.change_payment', 'api-auth/login')
def payments(request, loan_id):
    # TODO: results pagination for GET

    loan = get_object_or_404(Loan, loan_uuid=loan_id)

    if request.method == 'GET':
        payments = Payment.objects.filter(loan=loan)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        p = Payment(loan=loan)
        serializer = PaymentSerializer(instance=p, data=request.data)
        if serializer.is_valid():
            p = serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@login_required(login_url='api-auth/login')
def balance(request, loan_id):
    # TODO: Using a POST for a reading operation is only useful if we want to
    # avoid leaking sensitive information (eg. in server logs)
    # in this case the usage of POST is arguable
    if request.method == 'POST':
        if request.data.get('date'):
            balance = Balance(loan_id).calculate(request.data.get('date'))
            return Response({'balance': balance})
    return Response({}, status=status.HTTP_400_BAD_REQUEST)
