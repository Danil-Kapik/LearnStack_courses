from django.core.management.base import BaseCommand
from apps.courses.models import Tag


class Command(BaseCommand):
    help = "Populate the database with predefined tags"

    def handle(self, *args, **kwargs):
        tags_data = [
            # Уровень сложности
            "для начинающих",
            "средний уровень",
            "продвинутый уровень",
            "с нуля",
            # Формат обучения
            "видеоуроки",
            "интерактивные задания",
            "проектная работа",
            "с поддержкой ментора",
            "самостоятельный темп",
            # Сертификация и карьера
            "с сертификатом",
            "подготовка к собеседованию",
            "стажировка",
            "трудоустройство",
            # Технологии и инструменты
            "Django",
            "React",
            "PostgreSQL",
            "Docker",
            "TensorFlow",
            "PyTorch",
            "Kubernetes",
            "TypeScript",
            # Особенности курса
            "бесплатный",
            "премиум",
            "новый курс",
            "популярный",
            "акция",
            "живые вебинары",
            "сообщество студентов",
            # Язык контента
            "на русском",
            "на английском",
            "с субтитрами",
        ]

        for tag_name in tags_data:
            Tag.objects.get_or_create(name=tag_name)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Tag "{tag_name}" created or already exists'
                )
            )
