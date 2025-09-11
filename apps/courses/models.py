from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from apps.accounts.models import User

from .mixins import UniqueSlugMixin


# ========== Категории ==========
class Category(UniqueSlugMixin, MPTTModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="subcategories",
        on_delete=models.SET_NULL,
    )

    slug_from_field = "name"

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["tree_id", "lft"]

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


# ========== Теги ==========
class Tag(UniqueSlugMixin, models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    slug_from_field = "name"

    class Meta:
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name


# ========== Курсы ==========
class Course(UniqueSlugMixin, models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to="courses/images/", blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="courses"
    )
    instructor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"is_instructor": True},
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(help_text="в минутах")
    is_published = models.BooleanField(default=False)
    release_date = models.DateField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True)

    slug_from_field = "title"

    @property
    def rating(self):
        result = self.reviews.aggregate(avg_rating=models.Avg("rating"))
        return round(result["avg_rating"] or 0.0, 2)

    @property
    def students_count(self):
        return self.enrollments.count()

    def __str__(self):
        return self.title


# ========== Уроки ==========
class Lesson(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons"
    )
    title = models.CharField(max_length=255)
    video_url = models.URLField(blank=True, help_text="Ссылка на видеоурок")
    content = models.TextField(blank=True)
    duration = models.PositiveIntegerField(help_text="в минутах")
    order = models.PositiveIntegerField(blank=True, null=True)
    is_preview = models.BooleanField(default=False)

    class Meta:
        ordering = ["order"]
        unique_together = ("course", "order")

    def save(self, *args, **kwargs):
        if self.order is None:
            last_order = (
                Lesson.objects.filter(course=self.course).aggregate(
                    max_order=models.Max("order")
                )["max_order"]
                or 0
            )
            self.order = last_order + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


# # ========== 6. Отзывы ==========
# class Review(models.Model):
#     class RatingChoices(models.IntegerChoices):
#         ONE = 1, '1 - Ужасно'
#         TWO = 2, '2 - Плохо'
#         THREE = 3, '3 - Удовлетворительно'
#         FOUR = 4, '4 - Хорошо'
#         FIVE = 5, '5 - Отлично'

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     course = models.ForeignKey(
#         Course,
#         on_delete=models.CASCADE,
#         related_name='reviews')
#     rating = models.IntegerField(
#         choices=RatingChoices.choices,
#         default=5,
#         help_text='Выберите рейтинг',)
#     comment = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_moderated = models.BooleanField(default=False)

#     class Meta:
#         unique_together = ('user', 'course')
#         indexes = [models.Index(fields=['course', 'rating'])]

#     def __str__(self):
#         return f"{self.user} - {self.course} - {self.get_rating_display()}"


# # ========== 7. Записи на курс ==========
# class Enrollment(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='enrollments')
#     course = models.ForeignKey(
#         Course,
#         on_delete=models.CASCADE,
#         related_name='enrollments')
#     enrolled_at = models.DateTimeField(auto_now_add=True)
#     completed = models.BooleanField(default=False)

#     class Meta:
#         unique_together = ('user', 'course')
#         indexes = [models.Index(fields=['user', 'course'])]

#     @property
#     def progress_percent(self):
#         total_lessons = self.course.lessons.count()
#         if total_lessons == 0:
#             return 0.0

#         completed_lessons = LessonProgress.objects.filter(
#             user=self.user,
#             lesson__course=self.course,
#             completed=True
#         ).count()

#         return round((completed_lessons / total_lessons) * 100, 2)


# # ========== 8. Корзина ==========
# class CartItem(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='cart_items')
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     is_checked_out = models.BooleanField(default=False)
#     is_removed = models.BooleanField(default=False)
#     added_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user', 'course')


# # ========== 9. Покупки ==========
# class Purchase(models.Model):
#     class PaymentStatus(models.TextChoices):
#         PENDING = 'pending', 'Ожидает оплаты'
#         COMPLETED = 'completed', 'Завершено'
#         FAILED = 'failed', 'Неуспешно'
#         REFUNDED = 'refunded', 'Возвращено'
#         CANCELLED = 'cancelled', 'Отменено'
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='purchases'
#     )
#     course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     transaction_id = models.CharField(max_length=255, unique=True)
#     payment_status = models.CharField(
#         max_length=50,
#         choices=PaymentStatus.choices,
#         default=PaymentStatus.PENDING
#     )
#     purchased_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = "Покупка"
#         verbose_name_plural = "Покупки"

#     def __str__(self):
#         return (f"Покупка {self.course.title if self.course else 'N/A'} "
#                 f"пользователем {self.user.username} "
#                 f"- {self.get_payment_status_display()}")


# # ========== 10. Избранное ==========
# class Favorite(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='favorites')
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     added_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user', 'course')


# # ========== 11. Сертификаты ==========
# class Certificate(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     issued_at = models.DateTimeField(auto_now_add=True)
#     pdf_file = models.FileField(upload_to='certificates/')

#     class Meta:
#         unique_together = ('user', 'course')


# # ========== 13. Прогресс урока ==========
# class LessonProgress(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
#     completed = models.BooleanField(default=False)

#     class Meta:
#         unique_together = ('user', 'lesson')
