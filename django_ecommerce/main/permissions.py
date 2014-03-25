from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permissions(self, request, view, obj):
        
        #Allow all read type requests
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        #this leaves us with write requests (i.e. POST / PUT)
        return obj.user == request.user
