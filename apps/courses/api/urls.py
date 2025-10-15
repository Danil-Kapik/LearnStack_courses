from django.urls import path
from .views import ModuleOrderUpdateView

app_name = "api"

urlpatterns = [
    path(
        "<int:course_id>/modules/order/",
        ModuleOrderUpdateView.as_view(),
        name="module_order",
    ),
]
