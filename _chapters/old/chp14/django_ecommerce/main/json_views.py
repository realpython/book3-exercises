from rest_framework import mixins, generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from main.serializers import StatusReportSerializer, BadgeSerializer
from main.models import StatusReport, Badge
from main.permissions import IsOwnerOrReadOnly


class StatusCollection(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):

    queryset = StatusReport.objects.all()
    serializer_class = StatusReportSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class StatusMember(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   generics.GenericAPIView):

    queryset = StatusReport.objects.all()
    serializer_class = StatusReportSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BadgeCollection(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):

    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class BadgeMember(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
    mixins.DestroyModelMixin, generics.GenericAPIView
):

    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@api_view(('GET',))
def api_root(request):
    return Response({
        'status_reports': reverse(
            'status_reports_collection', request=request),
        'badges': reverse('badges_collection', request=request),
    })
