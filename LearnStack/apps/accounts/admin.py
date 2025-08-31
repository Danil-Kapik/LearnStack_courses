from django.contrib import admin
from django.utils.html import format_html
from .models import User, InstructorProfile


class InstructorProfileInline(admin.StackedInline):
    model = InstructorProfile
    can_delete = False
    fk_name = "user"
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "full_name",
        "email",
        "is_instructor",
        "created_at",
        "avatar_preview",
    )
    list_filter = ("is_instructor", "created_at")
    search_fields = ("username", "first_name", "last_name", "email")
    inlines = [InstructorProfileInline]
    readonly_fields = ("created_at", "updated_at", "slug")

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width:40px;/'
                ' height:40px; border-radius:50%;" />',
                obj.avatar.url,
            )
        return "—"

    avatar_preview.short_description = "Аватар"


@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "experience_short", "certifications_short")
    search_fields = ("user__first_name", "user__last_name", "user__username")
    readonly_fields = ("user",)

    def experience_short(self, obj):
        return (
            (obj.experience[:50] + "...")
            if len(obj.experience) > 50
            else obj.experience
        )

    experience_short.short_description = "Опыт"

    def certifications_short(self, obj):
        return (
            (obj.certifications[:50] + "...")
            if len(obj.certifications) > 50
            else obj.certifications
        )

    certifications_short.short_description = "Сертификаты"
