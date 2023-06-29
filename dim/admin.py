from django.contrib import admin
from .models import Model, Industry, AITag


class ModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'model_name', 'model_type', 'model_source')
    list_filter = ('model_name', 'model_type',)
    search_fields = ('model_name',)
    list_per_page = 20


class IndustryAdmin(admin.ModelAdmin):
    list_display = ('id', 'industry',)
    search_fields = ('industry',)
    list_per_page = 20


class AITagAdmin(admin.ModelAdmin):
    list_display = ('id', 'ai_tag', 'created_at')
    list_filter = ('ai_tag',)
    search_fields = ('ai_tag',)
    list_per_page = 20


admin.site.register(Model, ModelAdmin)
admin.site.register(Industry, IndustryAdmin)
admin.site.register(AITag, AITagAdmin)
