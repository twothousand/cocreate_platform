from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product.views import *

router = DefaultRouter()  # 可以处理视图的路由器
router.register('', ProductViewSet, 'product')  # 向路由器中注册视图集

urlpatterns = [
    # http://127.0.0.1:8000/api/team/
    # path("", include(router.urls)),
]
urlpatterns += router.urls  # 将路由器中的所以路由信息追到到django的路由列表中
