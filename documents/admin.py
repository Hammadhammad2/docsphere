from django.contrib import admin

from documents.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "project", "author", "created", "modified"]
    list_display_links = ["title"]
    search_fields = ["title", "body", "project__name"]
    list_filter = ["project", "created", "modified"]
    autocomplete_fields = ["project"]
    date_hierarchy = "created"
    ordering = ["-created"]
    list_per_page = 10
    list_max_show_all = 100
