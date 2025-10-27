from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from apps.students.views import RoleBasedLoginView


urlpatterns = [
    path("accounts/login/", RoleBasedLoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path(
        "courses/",
        include(("apps.courses.urls", "courses"), namespace="courses"),
    ),
    path(
        "students/",
        include(("apps.students.urls", "students"), namespace="students"),
    ),
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
