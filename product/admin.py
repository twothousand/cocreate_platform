from django.contrib import admin
from .models import Product, Version, Comment, Reply, Like, Collect


class ProductAdmin(admin.ModelAdmin):
    list_display = ('project', 'product_name')
    list_per_page = 20


class VersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'version_number', 'product_name')
    list_filter = ('model', 'industry', 'ai_tag', 'product_name')
    search_fields = ('product_name',)
    list_per_page = 20


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'comment_content', 'from_user_id')
    list_filter = ('product', 'from_user_id', 'comment_content')
    search_fields = ('comment_content',)
    list_per_page = 20


class ReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'reply_type', 'reply_content', 'from_user', 'to_user')
    list_filter = ('comment', 'from_user', 'to_user')
    search_fields = ('content',)
    list_per_page = 20


class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'liked_status')
    list_filter = ('product', 'user')
    search_fields = ()
    list_per_page = 20


class CollectAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'collect_status')
    list_filter = ('product', 'user')
    search_fields = ()
    list_per_page = 20


admin.site.register(Product, ProductAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Collect, CollectAdmin)
