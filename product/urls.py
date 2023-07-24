from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product.views import ProductViewSet

# 创建一个路由器并注册TeamViewSet和TeamMemberViewSet
router = DefaultRouter()


urlpatterns = [
    # 将router.urls添加到urlpatterns中
    path('', include(router.urls)),
    # 队伍管理：查询队员信息
    path('create_product_with_version/', ProductViewSet.as_view({'post': 'create_product_with_version'}), name='create_product_with_version'),
    path('update_product_with_version/', ProductViewSet.as_view({'put': 'update_product_with_version'}), name='update_product_with_version'),
    path('get_product_info/', ProductViewSet.as_view({'get': 'get_product_info'}), name='get_product_info'),
]
