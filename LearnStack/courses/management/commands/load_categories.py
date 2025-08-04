from django.core.management.base import BaseCommand
from courses.models import Category


class Command(BaseCommand):
    help = 'Loads initial categories into the database'

    def handle(self, *args, **options):
        categories_data = [
            {
                'name': 'Программирование',
                'subcategories': [
                    {'name': 'Веб-разработка (Frontend/Backend)'},
                    {'name': 'Мобильная разработка'},
                    {'name': 'Data Science & AI'},
                    {'name': 'Алгоритмы и структуры данных'},
                    {'name': 'Базы данных'},
                ]
            },
            {
                'name': 'Дизайн',
                'subcategories': [
                    {'name': 'Веб-дизайн'},
                    {'name': 'Графический дизайн'},
                    {'name': 'UX/UI'},
                    {'name': '3D-моделирование'},
                    {'name': 'Моушн-дизайн'},
                ]
            },
            {
                'name': 'Бизнес и маркетинг',
                'subcategories': [
                    {'name': 'Цифровой маркетинг'},
                    {'name': 'Управление проектами'},
                    {'name': 'Финансы и аналитика'},
                    {'name': 'Стартапы'},
                    {'name': 'Продажи'},
                ]
            }
        ]

        for category_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=category_data['name']
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category:\
                     {category.name} (slug: {category.slug})'))
            else:
                self.stdout.write(self.style.WARNING(f'Category exists:\
                     {category.name}'))

            for subcategory_data in category_data['subcategories']:
                subcategory, created = Category.objects.get_or_create(
                    name=subcategory_data['name'],
                    parent=category
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'\
                  └─ Created subcategory: {subcategory.name} (slug:\
                      {subcategory.slug})'))
                else:
                    self.stdout.write(self.style.WARNING(f'\
                  └─ Subcategory already exists: {subcategory.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully\
                                              loaded all categories!'))
