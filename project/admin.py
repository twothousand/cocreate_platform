from django.contrib import admin
from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'project_name', 'project_type', 'project_status', 'project_cycles',
        'project_creator', 'created_at', 'updated_at'
    ]
    filter_horizontal = ['model', 'industry', 'ai_tag']
    search_fields = ['project_name', 'project_description']
    list_filter = ['project_creator', 'model', 'industry', 'ai_tag', 'project_type', 'project_status']
    list_per_page = 10


admin.site.register(Project, ProjectAdmin)
