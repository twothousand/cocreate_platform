from django.shortcuts import render
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
# Create your views here.
# GET：列出所有项目，POST：创建新项目
from product.models import Product
from product.serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
