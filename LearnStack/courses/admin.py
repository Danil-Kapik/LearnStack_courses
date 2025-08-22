from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ("name", "slug", "parent")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    mptt_level_indent = 40  # Отступ для подкатегорий

    # Фильтр по родительским категориям
    list_filter = ("parent",)

    # Древовидное отображение
    mptt_indent_field = "name"
