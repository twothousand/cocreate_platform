from django.contrib import admin
from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'desc', 'tags', 'type', 'status', 'cycles', 'link', 'views', 'likes', 'favorites', 'post_datetime'
    )
    search_fields = ['name', 'desc']
    list_filter = ['tags', 'type', 'status']
    list_per_page = 10


admin.site.register(Project, ProjectAdmin)
