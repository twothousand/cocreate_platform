from rest_framework import serializers
from .models import Product, Version
from dim.models import Industry, Model, AITag
from function.models import Image


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

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

# 构建产品序列化器
class ProductSerializer(serializers.ModelSerializer):
    industry = IndustrySerializer(many=True)
    model = ModelSerializer(many=True)
    ai_tag = AITagSerializer(many=True)
    promotional_image = ImageSerializer(many=True)

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

# 产品详情序列化器
class ProductDetailSerializer(serializers.ModelSerializer):
    # 格式化时间
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    # 支持多对多关系的序列化
    model = serializers.SlugRelatedField(many=True, read_only=True, slug_field='model_name')
    industry = serializers.SlugRelatedField(many=True, read_only=True, slug_field='industry')
    ai_tag = serializers.SlugRelatedField(many=True, read_only=True, slug_field='ai_tag')


    class Meta:
        model = Product
        fields = '__all__'