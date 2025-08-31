from django.db import models
from django.contrib.auth.models import AbstractUser

from courses.mixins import UniqueSlugMixin


# ========== 1. Пользователь ==========
class User(UniqueSlugMixin, AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_instructor = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    avatar = models.ImageField(
        upload_to="avatars/%d/%m/%Y/",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    slug_from_field = "get_full_name"

    def get_full_name(self):
        name = f"{self.first_name} {self.last_name}".strip()
        return name if name else self.username

    @property
    def full_name(self):
        return self.get_full_name()

    def __str__(self):
        return self.get_full_name() or self.username


# ========== Профиль преподавателя ==========
class InstructorProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="instructor_profile"
    )
    experience = models.TextField(blank=True)
    social_links = models.JSONField(default=dict, blank=True)
    certifications = models.TextField(blank=True)

    def __str__(self):
        return f"Профиль: {self.user.full_name}"
