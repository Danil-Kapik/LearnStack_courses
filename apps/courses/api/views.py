from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db import transaction
from apps.courses.models import Course, Module


class ModuleOrderUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id, *args, **kwargs):
        # Получаем данные из запроса
        modules_data = request.data.get("order", [])

        if not course_id or not modules_data:
            return Response(
                {"error": "Missing 'course_id' or 'modules'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Проверяем, что курс существует
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response(
                {"error": "Course not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Проверка прав доступа
        if request.user != course.owner and not request.user.is_staff:
            return Response(
                {"error": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Загружаем все модули курса
        modules = {m.id: m for m in Module.objects.filter(course=course)}

        # Обновляем порядок модулей
        with transaction.atomic():
            for item in modules_data:
                module_id = int(item["id"])
                module = modules.get(module_id)
                if module:
                    module.order = int(item["order"])
            Module.objects.bulk_update(modules.values(), ["order"])

        return Response({"status": "ok"}, status=status.HTTP_200_OK)
