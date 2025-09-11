from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Tag, Course, Lesson


# === Category ===
@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ("name", "parent")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    mptt_level_indent = 40


# === Tag ===
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


# === Course ===
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "instructor",
        "price",
        "is_published",
        "release_date",
    )
    list_filter = ("is_published", "category", "tags")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    date_hierarchy = "release_date"
    autocomplete_fields = ("category", "instructor")


# === Lesson ===
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order", "duration", "is_preview")
    list_filter = ("course", "is_preview")
    search_fields = ("title", "content")
    ordering = ("course", "order")


# from django.contrib import admin
# from mptt.admin import MPTTModelAdmin
# from .models import Category


# @admin.register(Category)
# class CategoryAdmin(MPTTModelAdmin):
#     list_display = ("name", "slug", "parent")
#     search_fields = ("name", "slug")
#     prepopulated_fields = {"slug": ("name",)}
#     mptt_level_indent = 40  # Отступ для подкатегорий

#     # Фильтр по родительским категориям
#     list_filter = ("parent",)

#     # Древовидное отображение
#     mptt_indent_field = "name"
