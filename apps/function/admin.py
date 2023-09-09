from django.contrib import admin
from .models import Image, System


# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_url', 'created_at')
    search_fields = ('image_url',)
    list_per_page = 20


class SystemAdmin(admin.ModelAdmin):
    list_display = ('id', 'system_page', 'content_name', 'content_name_en', 'content_title', 'system_text', 'system_json', 'created_at', 'updated_at')  # 在列表中显示的字段
    list_filter = ('content_name',)  # 添加筛选器，可根据内容类型过滤
    search_fields = ('id', 'content_name')  # 添加搜索字段，可根据ID或内容类型搜索


admin.site.register(Image, ImageAdmin)
admin.site.register(System, SystemAdmin)
