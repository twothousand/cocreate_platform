# django
from django.db.models import Count

# rest_framework
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

# common
from common.mixins import my_mixins
from common.utils.decorators import disallow_methods

# app
from apps.notification.models import Message, MessageTemplate
from apps.notification.serializer import MessageSerializer
from apps.user.permissions import IsMessageReceiver

from collections import defaultdict

# 自定义分页器
class CustomPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100


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
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsMessageReceiver, IsAuthenticated]
    pagination_class = CustomPagination  # 自定义分页器

    @action(methods=['GET'], detail=True)
    def get_unread_message_count(self, request):
        try:
            user = request.user
            all_message_categories = MessageTemplate.get_all_message_categories()
            message_type_data = defaultdict(int)  # 初始化一个默认值为0的字典

            unread_count_by_type = Message.objects.filter(receiver=user, is_read=False).values(
                'message_template__message_category').annotate(unread_count=Count('id'))
            for category in all_message_categories:
                for item in unread_count_by_type:
                    if item['message_template__message_category'] == category:
                        message_type_data[category] = item['unread_count']
                    else:
                        message_type_data[category] = 0

            total_unread_count = sum(item['unread_count'] for item in unread_count_by_type)

            # message_type_data = {
            #     item['message_template__message_category']: item['unread_count']
            #     for item in unread_count_by_type
            # }

            response_data = {
                'message': '成功获取未读消息数量',
                'data': {'total': total_unread_count,
                        'unread_message_count_by_type': dict(message_type_data)
                         }
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            response_data = {
                'message': '获取未读消息数量失败',
                'data': {'errors': str(e)}
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['GET'], detail=True)
    def get_message_by_type(self, request, *args, **kwargs):
        """
        获取所有未删除的消息通知列表
        @param request:
        @param args:
        @param kwargs:
        @return:
        """
        # 过滤消息，只获取当前用户作为接收者的消息
        message_type = self.request.GET.get('message_type')
        messages = Message.objects.filter(receiver=request.user, is_deleted=False, message_template__message_type=message_type).all()

        # 使用 DRF 的内置分页
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # 如果没有分页（例如，分页被禁用），则直接返回所有消息
        serializer = self.get_serializer(messages, many=True)
        response_data = {
            'message': '已成功获取消息(未分页)',
            'data': serializer.data
        }

        # paginated_queryset = self.paginate_queryset(queryset)
        # serializer = serializers.ProjectDetailSerializer(paginated_queryset, many=True)

        return Response(response_data)

    @action(methods=['GET'], detail=True)
    def get_message_by_category(self, request, *args, **kwargs):
        """
        获取所有未删除的消息通知列表
        @param request:
        @param args:
        @param kwargs:
        @return:
        """
        # 过滤消息，只获取当前用户作为接收者的消息
        message_category = self.request.GET.get('message_category')
        messages = Message.objects.filter(receiver=request.user, is_deleted=False, message_template__message_category=message_category).all()

        # 使用 DRF 的内置分页
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # 如果没有分页（例如，分页被禁用），则直接返回所有消息
        serializer = self.get_serializer(messages, many=True)
        response_data = {
            'message': '已成功获取消息(未分页)',
            'data': serializer.data
        }

        # paginated_queryset = self.paginate_queryset(queryset)
        # serializer = serializers.ProjectDetailSerializer(paginated_queryset, many=True)

        return Response(response_data)