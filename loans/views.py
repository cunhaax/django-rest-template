from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Loan
from .serializers import LoanSerializer


@api_view(['GET', 'POST'])
def loans(request):
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
