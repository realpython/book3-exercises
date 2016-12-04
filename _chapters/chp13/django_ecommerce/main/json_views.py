from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from main.serializers import StatusReportSerializer
from main.models import StatusReport


@api_view(['GET', 'POST'])
def status_collection(request):
    """Get the collection of all status_reports
    or create a new one"""

    if request.method == 'GET':
        status_report = StatusReport.objects.all()
        serializer = StatusReportSerializer(status_report, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = StatusReportSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def status_member(request, id):
    """Get, update or delete a status_report instance"""

    try:
        status_report = StatusReport.objects.get(id=id)
    except StatusReport.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StatusReportSerializer(status_report)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = StatusReportSerializer(status_report, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        status_report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
