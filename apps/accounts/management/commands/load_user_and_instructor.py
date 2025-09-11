from django.core.management.base import BaseCommand
from apps.accounts.models import User, InstructorProfile


class Command(BaseCommand):
    help = (
        "Создаёт пользователей до 10 шт. и назначает 5 из них преподавателями"
    )

    def handle(self, *args, **kwargs):
        users = []

        # Создание недостающих пользователей (до 10)
        total_needed = 10
        current_count = User.objects.count()
        to_create = max(0, total_needed - current_count)

        for i in range(current_count + 1, current_count + to_create + 1):
            first_name = f"Имя{i}"
            last_name = f"Фамилия{i}"
            username = f"user{i}"
            email = f"user{i}@example.com"

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "bio": f"Краткая биография пользователя {i}",
                },
            )
            if created:
                user.set_password("password123")
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Создан пользователь: {username}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Пользователь {username} уже существует"
                    )
                )

            users.append(user)

        # Убедимся, что есть 5 преподавателей
        instructors = User.objects.filter(is_instructor=True).count()
        need_instructors = max(0, 5 - instructors)

        if need_instructors > 0:
            # выбираем пользователей без статуса преподавателя
            candidates = User.objects.filter(is_instructor=False)[
                :need_instructors
            ]
            for user in candidates:
                user.is_instructor = True
                user.save()
                InstructorProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        "experience": f"Опыт преподавания {user.id} лет",
                        "social_links": {
                            "vk": f"https://vk.com/instructor{user.id}",
                            "telegram": f"https://t.me/instructor{user.id}",
                        },
                        "certifications": f"Сертификат №{1000+user.id}",
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Назначен преподаватель: {user.username}"
                    )
                )
        else:
            self.stdout.write(
                self.style.WARNING("Уже есть как минимум 5 преподавателей")
            )
