from django.urls import path, include
from rest_framework.routers import DefaultRouter
from function.views import ImageViewSet

# 创建一个路由器并注册TeamViewSet和TeamMemberViewSet
router = DefaultRouter()


urlpatterns = [
    # 将router.urls添加到urlpatterns中
    path('', include(router.urls)),
    # 上传图片
    path('upload_image/', ImageViewSet.as_view({'post': 'upload_image'}), name='upload_image'),
]