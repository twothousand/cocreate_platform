from rest_framework import serializers
from .models import Product, Version
from dim.models import Industry, Model, AITag


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = '__all__'


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'


class AITagSerializer(serializers.ModelSerializer):
    class Meta:
        model = AITag
        fields = '__all__'


# 构建产品序列化器
class ProductSerializer(serializers.ModelSerializer):
    industry = IndustrySerializer(many=True)
    model = ModelSerializer(many=True)
    ai_tag = AITagSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = "__all__"


class VersionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = "__all__"


class ImageUploadSerializer(serializers.Serializer):
    file = serializers.ImageField()
