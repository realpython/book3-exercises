from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from usermap.models import UserLocation
import json


@api_view(['GET', 'POST'])
def user_locations_list(request):
    if request.method == 'GET':
        locations = json.loads(UserLocation.objects().to_json())
        return Response(locations)
    if request.method == 'POST':
        locations - UserLocation().from_json(json.dumps(request.DATA))
        locations.save()
        return Response(
            json.loads(locations.to_json()),
            status=status.HTTP_201_CREATED
        )
