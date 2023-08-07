# rest_framework
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# common
from common.mixins import my_mixins

# app
from notification.models import Message
from notification.serializer import MessageSerializer


# Create your views here.
class MessageViewSet(my_mixins.CustomResponseMixin, my_mixins.RetrieveUpdateListModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

