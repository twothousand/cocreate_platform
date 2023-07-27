from .models import Feedback
from .serializers import FeedbackSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from user.models import User
from project.models import Project
from django.shortcuts import get_object_or_404
from django.db.models import Q
from datetime import date

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class FeedbackViewSet(ModelViewSet):
    # 接口：创建产品反馈（POST）
    @action(methods=['POST'], detail=True)
    def create_feedback(self, request, *args, **kwargs):
        try:
            # Extract data from the request data
            feedback_data = request.data
            # Get the current user
            current_user_instance = get_object_or_404(User, id=feedback_data['user_id'])

            # Create the feedback instance
            feedback_instance = Feedback.objects.create(
                user=current_user_instance,
                feedback_type=feedback_data['feedback_type'],
                feedback_email=feedback_data['feedback_email'],
                feedback_content=feedback_data['feedback_content']
            )

            # Serialize and return the data
            feedback_serializer = FeedbackSerializer(feedback_instance)  # Replace 'FeedbackSerializer' with your actual serializer
            response_data = {
                'message': '产品反馈创建成功',
                'data': {
                    'feedback': feedback_serializer.data,
                },
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            response_data = {
                'message': '创建产品反馈失败',
                'data': {'errors': str(e)}
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
