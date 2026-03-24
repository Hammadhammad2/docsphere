from django.contrib import admin

from projects.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "organization", "created", "modified"]
    list_display_links = ["name"]
    search_fields = ["name", "description", "organization__name"]
    list_filter = ["organization", "created", "modified"]
    autocomplete_fields = ["organization"]
    date_hierarchy = "created"
    ordering = ["-created"]
    list_per_page = 10
    list_max_show_all = 100
