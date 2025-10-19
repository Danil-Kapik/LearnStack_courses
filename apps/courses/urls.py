from django.urls import path, include
from . import views

app_name = "courses"

urlpatterns = [
    path("list/", views.ManageCourseListView.as_view(), name="manage"),
    path(
        "create/",
        views.CourseCreateView.as_view(),
        name="create",
    ),
    path(
        "<pk>/update/",
        views.CourseUpdateView.as_view(),
        name="update",
    ),
    path(
        "<pk>/delete/",
        views.CourseDeleteView.as_view(),
        name="delete",
    ),
    path(
        "<pk>/module/",
        views.CourseModuleUpdateView.as_view(),
        name="module_update",
    ),
    path(
        "module/<int:module_id>/content/<model_name>/create/",
        views.ContentCreateUpdateView.as_view(),
        name="content_create",
    ),
    path(
        "module/<int:module_id>/content/<model_name>/<id>/",
        views.ContentCreateUpdateView.as_view(),
        name="content_update",
    ),
    path(
        "content/<int:id>/delete/",
        views.ContentDeleteView.as_view(),
        name="content_delete",
    ),
    path(
        "module/<int:module_id>/",
        views.ModuleContentListView.as_view(),
        name="content_list",
    ),
    path("", views.CourseListView.as_view(), name="list"),
    path(
        "subject/<slug:subject>/",
        views.CourseListView.as_view(),
        name="list_subject",
    ),
    path("<slug:slug>/", views.CourseDetailView.as_view(), name="detail"),
    # Подключаем REST API
    path("api/", include("apps.courses.api.urls", namespace="api")),
]
