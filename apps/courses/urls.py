from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path("list/", views.ManageCourseListView.as_view(), name="list"),
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
]
