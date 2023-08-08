# rest_framework
from rest_framework.permissions import IsAuthenticated

# common
from common.mixins import my_mixins
from common.utils.decorators import disallow_methods

# app
from notification.models import Message
from notification.serializer import MessageSerializer


# Create your views here.
class MessageViewSet(my_mixins.CustomResponseMixin, my_mixins.RetrieveUpdateListModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    @disallow_methods(['PUT'])
    def dispatch(self, request, *args, **kwargs):
        return super(MessageViewSet, self).dispatch(request, *args, **kwargs)