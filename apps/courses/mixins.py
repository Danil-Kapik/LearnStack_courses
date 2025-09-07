from slugify import slugify
from django.db import models


class UniqueSlugMixin(models.Model):
    slug_field_name = 'slug'
    slug_from_field = 'name'

    class Meta:
        abstract = True

    def generate_unique_slug(self):
        field_value = getattr(self, self.slug_from_field)

        # Если значение — это метод
        if callable(field_value):
            field_value = field_value()

        base_slug = slugify(field_value)
        slug = base_slug
        ModelClass = self.__class__
        counter = 1
        while ModelClass.objects.filter(**{self.slug_field_name: slug}).\
                exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def save(self, *args, **kwargs):
        slug_value = getattr(self, self.slug_field_name, None)
        if not slug_value:
            setattr(self, self.slug_field_name, self.generate_unique_slug())
        super().save(*args, **kwargs)
