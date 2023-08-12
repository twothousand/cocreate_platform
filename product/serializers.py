from rest_framework import serializers
from .models import Product, Version
from dim.models import Industry, Model, AITag
from function.models import Image


# 构建产品序列化器
class ProductSerializer(serializers.ModelSerializer):
    # 支持多对多关系的序列化
    model = serializers.SlugRelatedField(many=True, read_only=True, slug_field='model_name')
    industry = serializers.SlugRelatedField(many=True, read_only=True, slug_field='industry')
    ai_tag = serializers.SlugRelatedField(many=True, read_only=True, slug_field='ai_tag')
    promotional_image = serializers.SlugRelatedField(many=True, read_only=True, slug_field='image_url')

    # 获取外键图片的url
    product_display_qr_code_url = serializers.SerializerMethodField()
    test_group_qr_code_url = serializers.SerializerMethodField()

    def get_product_display_qr_code_url(self, instance):
        return instance.product_display_qr_code.image_url if instance.product_display_qr_code else None

    def get_test_group_qr_code_url(self, instance):
        return instance.test_group_qr_code.image_url if instance.test_group_qr_code else None

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
    promotional_image = serializers.SlugRelatedField(many=True, read_only=True, slug_field='image_url')

    # 获取外键图片的url
    product_display_qr_code_url = serializers.SerializerMethodField()
    test_group_qr_code_url = serializers.SerializerMethodField()

    def get_product_display_qr_code_url(self, instance):
        return instance.product_display_qr_code.image_url if instance.product_display_qr_code else None

    def get_test_group_qr_code_url(self, instance):
        return instance.test_group_qr_code.image_url if instance.test_group_qr_code else None

    class Meta:
        model = Product
        fields = '__all__'
