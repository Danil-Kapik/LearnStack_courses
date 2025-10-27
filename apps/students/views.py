from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .forms import CourseEnrollForm
from apps.courses.models import Course


class RoleBasedLoginView(LoginView):
    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy("courses:manage")
        return reverse_lazy("students:course_list")


class StudentRegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = "students/student/registration_form.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = False
        user.is_superuser = False
        user.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy("courses:manage")
        return reverse_lazy("students:course_list")


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data["course"]
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("students:course_detail", args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "students/course/list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "students/course/detail.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # получить текущий курс
        course = self.get_object()
        if "module_id" in self.kwargs:
            # загрузить конкретный модуль
            context["module"] = course.modules.get(id=self.kwargs["module_id"])
        else:
            # загрузить первый модуль
            context["module"] = course.modules.all()[0]
        return context
