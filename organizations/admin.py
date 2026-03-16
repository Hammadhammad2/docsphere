from django.contrib import admin

from organizations.models import Organization

# Register your models here.


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "created", "modified"]
    search_fields = ["name", "description"]
    list_filter = ["created", "modified"]
    date_hierarchy = "created"
    ordering = ["-created"]
    list_per_page = 10
    list_max_show_all = 100
    list_editable = ["description"]
    list_display_links = ["name"]
