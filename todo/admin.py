from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'priority', 'is_completed', 'created_at', 'updated_at')
    list_filter = ('genre', 'priority', 'is_completed')
    search_fields = ('title', 'memo')
    ordering = ('-created_at',)
