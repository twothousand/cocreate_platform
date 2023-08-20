from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product.views import ProductViewSet, ProductFilterAndSearchView

router = DefaultRouter()


urlpatterns = [
    # 将router.urls添加到urlpatterns中
    path('', include(router.urls)),
    # 产品搜索
    path('filter-search', ProductFilterAndSearchView.as_view({'get': 'search_filter_products'}), name='product-filter-and-search'),
    # 产品初次发布（POST），同时更新产品版本信息
    path('create_product_with_version/', ProductViewSet.as_view({'post': 'create_product_with_version'}), name='create_product_with_version'),
    # 更新产品信息（PUT），同时更新产品版本信息
    path('update_product_with_version/', ProductViewSet.as_view({'put': 'update_product_with_version'}), name='update_product_with_version'),
    # 获取产品信息（GET）
    path('get_product_info/<str:product_id>/', ProductViewSet.as_view({'get': 'get_product_info'}), name='get_product_info'),
    # 获取产品ID（GET）
    path('get_product_id/<str:project_id>/', ProductViewSet.as_view({'get': 'get_product_id'}), name='get_product_id'),
]
