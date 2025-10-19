from django.urls import path

from . import views

app_name = "students"
urlpatterns = [
    path(
        "register/",
        views.StudentRegistrationView.as_view(),
        name="registration",
    ),
    path(
        "enroll-course/",
        views.StudentEnrollCourseView.as_view(),
        name="enroll_course",
    ),
    path(
        "courses/",
        views.StudentCourseListView.as_view(),
        name="course_list",
    ),
    path(
        "courses/<pk>/",
        views.StudentCourseDetailView.as_view(),
        name="course_detail",
    ),
    path(
        "courses/<pk>/<module_id>/",
        views.StudentCourseDetailView.as_view(),
        name="module_content",
    ),
]
