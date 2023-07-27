from django.contrib import admin
from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'feedback_type', 'feedback_email', 'feedback_content')
    list_filter = ('user', 'feedback_type', 'feedback_email')
    list_per_page = 20


admin.site.register(Feedback, FeedbackAdmin)
