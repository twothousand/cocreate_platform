from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.feedback.views import FeedbackViewSet

router = DefaultRouter()

urlpatterns = [
    # 将router.urls添加到urlpatterns中
    path('', include(router.urls)),
    # 创建反馈（POST）
    path('create_feedback/', FeedbackViewSet.as_view({'post': 'create_feedback'}), name='create_feedback'),
]
