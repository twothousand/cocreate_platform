# django
from django.db.models import Count

# rest_framework
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

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


# 消息查询
class MessageQueryView(my_mixins.LoggerMixin, my_mixins.CreatRetrieveUpdateModelViewSet):

    @action(methods=['GET'], detail=True)
    def get_unread_message_count(self, request):
        permission_classes = [IsAuthenticated]
        try:
            user = request.user
            unread_count_by_type = Message.objects.filter(receiver=user, is_read=False).values(
                'message_template__message_type').annotate(unread_count=Count('id'))

            total_unread_count = sum(item['unread_count'] for item in unread_count_by_type)

            message_type_data = {
                item['message_template__message_type']: item['unread_count']
                for item in unread_count_by_type
            }

            response_data = {
                'message': '成功获取未读消息数量',
                'data': {'total': total_unread_count,
                        'unread_message_count_by_type': message_type_data
                         }
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            response_data = {
                'message': '获取未读消息数量失败',
                'data': {'errors': str(e)}
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
