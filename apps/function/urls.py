# django
from django.urls import path, include
# rest_framework
from rest_framework.routers import DefaultRouter
# function
from apps.function import views

router = DefaultRouter()

urlpatterns = [
    # 将router.urls添加到urlpatterns中
    path('', include(router.urls)),
    # 上传图片
    path('upload_image/', views.ImageViewSet.as_view({'post': 'upload_image'}), name='upload_image'),
    path('delete_image/', views.ImageViewSet.as_view({'delete': 'delete_image'}), name='delete_image'),
    # http://127.0.0.1:8000/api/users/sendsms/  # 发送短信验证码
    path('send_sms/', views.VerifCodeViewSet.as_view({'post': 'create'})),
    path('send_sms_test/', views.VerifCodeViewSet.as_view({'post': 'send_sms_test'})),
    path('get_system_content/', views.SystemView.as_view({'get': 'get_system_content'}), name='get_system_content'),
]
