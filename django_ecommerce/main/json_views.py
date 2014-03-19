from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from main.serializers import Status_Reports_Serializer
from main.models import Status_Reports


@api_view(['GET','POST'])
def status_collection(request):
    '''get the collection of all status_reports
    or create a new one'''

    if request.method == 'GET':
        status = Status_Reports.objects.all()
        serializer = Status_Reports_Serializer(status, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = Status_Reports_Serializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)

