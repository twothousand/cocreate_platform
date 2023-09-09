from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import model_view, industry_view, ai_tag_view

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('model/', model_view, name='models'),
    path('industry/', industry_view, name='industries'),
    path('ai_tag/', ai_tag_view, name='ai_tags'),
]
