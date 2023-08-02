from django.contrib import admin
from function.models import Image


# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_url', 'created_at')
    search_fields = ('image_url',)
    list_per_page = 20


admin.site.register(Image, ImageAdmin)
