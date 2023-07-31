from rest_framework import serializers
from dim.models import Image
from dim.models import Industry, Model, AITag


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

