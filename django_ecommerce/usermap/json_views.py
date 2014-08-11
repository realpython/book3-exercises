from rest_framework import status, mixins, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
#from usermap.serializers import UserLocationSerializer
from usermap.models import UserLocation
import json


@api_view(['GET', 'POST'])
def user_locations_list(request):
    if request.method == 'GET':
        locs = json.loads(UserLocation.objects().to_json())
        return Response(locs)
        #return HttpResponse(UserLocation.objects().to_json(), content_type="application/json")
    if request.method == 'POST':
        print(str(request.DATA))
        loc = UserLocation().from_json(json.dumps(request.DATA))
        loc.save()
        return Response(json.loads(loc.to_json()), status=status.HTTP_201_CREATED)




'''
class UserLocationCollection(mixins.ListModelMixin,
                             mixins.CreateModelMixin,
                             generics.GenericAPIView):

    #queryset = UserLocation.objects()
    #serializer_class = UserLocationSerializer
    
    def get(self, request):
        data = UserLocation.objects()
        return Response(data.to_json())

    def post(self, request):
        return self.create(request)
'''
