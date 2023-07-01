from django.contrib import admin
from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'project_name', 'project_description', 'project_tags', 'project_type', 'project_status', 'project_cycles',
        'project_source_link', 'model', 'industry', 'ai_tag'
    ]
    search_fields = ['project_name', 'project_description']
    list_filter = ['project_creator', 'project_tags', 'project_type', 'project_status']
    list_per_page = 10


admin.site.register(Project, ProjectAdmin)
