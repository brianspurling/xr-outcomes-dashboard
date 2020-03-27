from django.contrib import admin

from .models import Commentary

@admin.register(Commentary)
class CommentaryAdmin(admin.ModelAdmin):
    list_display = ['chart_name']
    ordering = ('chart_name',)
    search_fields = ('chart_name', 'commentary_text')
    readonly_fields = ["chart_name"]
