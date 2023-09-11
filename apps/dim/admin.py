from django.contrib import admin
from apps.dim.models import Model, Industry, AITag


class ModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'model_name', 'model_type', 'model_source', 'is_open_source', 'created_at')
    list_filter = ('model_name', 'model_type', 'model_source', 'is_open_source')
    search_fields = ('model_name',)
    list_per_page = 20


class IndustryAdmin(admin.ModelAdmin):
    list_display = ('id', 'industry', 'created_at')
    search_fields = ('industry',)
    list_per_page = 20


class AITagAdmin(admin.ModelAdmin):
    list_display = ('id', 'ai_tag', 'created_at')
    search_fields = ('ai_tag',)
    list_per_page = 20


admin.site.register(Model, ModelAdmin)
admin.site.register(Industry, IndustryAdmin)
admin.site.register(AITag, AITagAdmin)
