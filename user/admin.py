# django库
from django.contrib import admin
# app
from .models import User

admin.site.site_header = "AIGC共创平台 后台管理界面"
admin.site.site_title = "后台管理界面"


class UserManager(admin.ModelAdmin):
    list_display = ['username', 'email', 'nickname', 'name']
    list_filter = ['username', 'nickname', 'name']
    search_fields = ['username', 'nickname', 'name']
    list_per_page = 10


admin.site.register(User, UserManager)
