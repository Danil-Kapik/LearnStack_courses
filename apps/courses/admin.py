from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Subject, Course, Module


@admin.register(Subject)
class SubjectAdmin(MPTTModelAdmin):
    list_display = ["title", "slug"]
    prepopulated_fields = {"slug": ("title",)}
    mptt_level_indent = 40


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "subject", "created"]
    list_filter = ["created", "subject"]
    search_fields = ["title", "overview"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ModuleInline]
