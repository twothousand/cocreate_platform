from django.contrib import admin
from apps.feedback.models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'feedback_type', 'feedback_contact', 'feedback_content')
    list_filter = ('feedback_type', 'feedback_contact')
    list_per_page = 20


admin.site.register(Feedback, FeedbackAdmin)
