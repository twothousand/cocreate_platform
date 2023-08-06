# 系统模块

# django
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth import get_user_model
# rest_framework
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
# common
from common.mixins import my_mixins
from common.utils import aliyun_green
# app
from user.permissions import IsOwnerOrReadOnly
from feedback.models import Feedback
from feedback.serializers import FeedbackSerializer

User = get_user_model()


class FeedbackViewSet(my_mixins.LoggerMixin, my_mixins.CreatRetrieveUpdateModelViewSet):
    serializer_class = FeedbackSerializer
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:  # 对于POST、PUT和DELETE请求
            permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]  # 需要用户被认证
        else:  # 对于其他请求方法，比如GET、PATCH等
            permission_classes = [AllowAny]  # 允许任何人，不需要身份验证
        return [permission() for permission in permission_classes]

    # 创建产品反馈
    @transaction.atomic
    @action(methods=['POST'], detail=True)
    def create_feedback(self, request, *args, **kwargs):
        try:
            feedback_data = request.data
            user_id = request.user.id
            current_user_instance = get_object_or_404(User, id=user_id)
            # 校验反馈信息是否内容合规
            s = aliyun_green.AliyunModeration()
            check_res = s.text_moderation("chat_detection",
                                          feedback_data['feedback_content'])
            if check_res['code'] != 1:
                response_data = {
                    'message': '文本检测违规:' + check_res['message'],
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            feedback_instance = Feedback.objects.create(
                user=current_user_instance,
                feedback_type=feedback_data['feedback_type'],
                feedback_email=feedback_data['feedback_email'],
                feedback_content=feedback_data['feedback_content']
            )
            feedback_serializer = FeedbackSerializer(feedback_instance)
            response_data = {
                'message': '产品反馈创建成功',
                'data': {
                    'feedback': feedback_serializer.data,
                },
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # 显式地触发回滚操作
            transaction.set_rollback(True)
            response_data = {
                'message': '创建产品反馈失败',
                'data': {'errors': str(e)}
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
