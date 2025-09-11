from django.core.management.base import BaseCommand
from apps.courses.models import Category


CATEGORIES = {
    "Программирование": {
        "Python": [
            "Основы Python",
            "Веб-разработка (Django/FastAPI)",
            "Data Science (Pandas/NumPy)",
            "Автоматизация и скрипты",
        ],
        "☕ Java": [
            "Java Core",
            "Spring Framework",
            "Android Development",
        ],
        "JavaScript": [
            "React",
            "Node.js",
            "Vue.js",
            "Angular",
        ],
        "Rust": [
            "Основы Rust",
            "Системное программирование",
            "WebAssembly",
        ],
    },
    "Data Science & AI": {
        "Машинное обучение": [
            "Нейронные сети",
            "Computer Vision",
            "NLP",
        ],
        "Анализ данных": [
            "SQL и базы данных",
            "Tableau/Power BI",
            "Excel для аналитиков",
        ],
        "Big Data": [
            "Hadoop/Spark",
            "Data Engineering",
            "Cloud Data Solutions",
        ],
    },
    "DevOps & Администрирование": {
        "Linux/Unix": [],
        "Docker & Kubernetes": [],
        "Git и системы контроля версий": [],
        "CI/CD": [],
        "Cloud Platforms": [
            "AWS",
            "Azure",
            "Google Cloud",
        ],
    },
    "Frontend & Дизайн": {
        "UI/UX Design": [],
        "Responsive Web Design": [],
        "Progressive Web Apps": [],
        "Animation & Graphics": [],
    },
}


class Command(BaseCommand):
    help = "Загружает категории в базу данных"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Загрузка категорий..."))

        def create_category(name, parent=None):
            category, created = Category.objects.get_or_create(
                name=name,
                parent=parent,
            )
            if created:
                self.stdout.write(f"✔ Создана категория: {name}")
            return category

        for root_name, subcats in CATEGORIES.items():
            root = create_category(root_name)
            for sub_name, leafs in subcats.items():
                sub = create_category(sub_name, parent=root)
                for leaf in leafs:
                    create_category(leaf, parent=sub)

        self.stdout.write(
            self.style.SUCCESS("Все категории успешно загружены.")
        )
