from slugify import slugify
from django.db import models
from django.db import transaction


class UniqueSlugMixin(models.Model):
    slug_field_name = "slug"
    slug_from_field = "name"

    class Meta:
        abstract = True

    def generate_unique_slug(self):
        """Генерирует уникальный slug, безопасный для
        использования при создании модели"""
        field_value = getattr(self, self.slug_from_field)

        if callable(field_value):
            field_value = field_value()

        return slugify(field_value)

    def save(self, *args, **kwargs):
        # Генерируем slug только если он не задан
        if not getattr(self, self.slug_field_name, None):
            base_slug = self.generate_unique_slug()
            final_slug = self._get_unique_slug_from_db(base_slug)
            setattr(self, self.slug_field_name, final_slug)
        super().save(*args, **kwargs)

    def _get_unique_slug_from_db(self, base_slug):
        """Получает уникальный slug из базы данных
        (выполняется только при save)"""
        slug = base_slug
        ModelClass = self.__class__
        counter = 1

        # Используем атомарную транзакцию для безопасности
        with transaction.atomic():
            while (
                ModelClass.objects.filter(**{self.slug_field_name: slug})
                .exclude(pk=getattr(self, "pk", None))
                .exists()
            ):
                slug = f"{base_slug}-{counter}"
                counter += 1

        return slug
