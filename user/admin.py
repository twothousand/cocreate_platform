# django库
from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

admin.site.site_header = "AIGC共创平台 后台管理界面"
admin.site.site_title = "后台管理界面"


class UserManager(admin.ModelAdmin):
    list_display = ['username', 'id', 'email', 'name', 'nickname', 'biography', 'professional_career', 'location']
    search_fields = ['username', 'nickname', 'name']
    list_filter = ['location', 'professional_career']
    list_per_page = 10


admin.site.register(User, UserManager)
