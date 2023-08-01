from rest_framework import serializers
from dim.models import Image
from dim.models import Industry, Model, AITag


class ImageSerializer(serializers.ModelSerializer):
    TYPE_CHOICES = (
        ('avatar', 'avatar'),
        ('project', 'project'),
        ('product', 'product'),
    )
    category = serializers.ChoiceField(choices=TYPE_CHOICES, required=True, allow_blank=True)

    class Meta:
        model = Image
        fields = '__all__'
