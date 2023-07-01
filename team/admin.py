from django.contrib import admin
from .models import Team, Application, Member


class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'team_leader', 'created_at')
    search_fields = ('team_leader',)
    list_per_page = 20


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'project', 'status', 'created_at')
    list_filter = ('user', 'project', 'status')
    search_fields = ('user', 'project')
    list_per_page = 20


class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'team', 'is_leader', 'member_status', 'user_id')
    list_filter = ('team',)
    search_fields = ('team',)
    list_per_page = 20


admin.site.register(Team, TeamAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Member, MemberAdmin)
