# rest_framework
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# common
from common.mixins import my_mixins
from common.utils.decorators import disallow_methods

# app
from notification.models import Message
from notification.serializer import MessageSerializer
from user.permissions import IsMessageReceiver


# Create your views here.
class MessageViewSet(my_mixins.CustomResponseMixin, my_mixins.RetrieveUpdateDestroyListModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsMessageReceiver, IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        获取所有未删除的消息通知列表
        @param request:
        @param args:
        @param kwargs:
        @return:
        """
        # 过滤消息，只获取当前用户作为接收者的消息
        messages = Message.get_all_messages(request.user)

        # 使用 DRF 的内置分页
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # 如果没有分页（例如，分页被禁用），则直接返回所有消息
        serializer = self.get_serializer(messages, many=True)

        return Response(serializer.data)

    def perform_destroy(self, instance):
        """
        逻辑删除
        @param instance:
        @return:
        """
        instance.delete()

    @disallow_methods(['PUT'])
    def dispatch(self, request, *args, **kwargs):
        return super(MessageViewSet, self).dispatch(request, *args, **kwargs)