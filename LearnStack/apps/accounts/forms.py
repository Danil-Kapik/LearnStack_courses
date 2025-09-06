# from django.contrib.auth.forms import UserCreationForm

# from .models import User


# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = UserCreationForm.Meta.fields + (
#             "email",
#             "first_name",
#             "last_name",
#         )

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, InstructorProfile


class RegistrationForm(UserCreationForm):
    ROLE_CHOICES = [
        ("student", "Я студент"),
        ("instructor", "Я преподаватель"),
    ]
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        initial="student",
    )

    # поля для преподавателя
    experience = forms.CharField(
        widget=forms.Textarea, required=False, label="Опыт преподавания"
    )
    certifications = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label="Сертификаты и квалификации",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "avatar",
        )

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")

        if role == "instructor":
            if not cleaned_data.get("experience"):
                self.add_error("experience", "Укажите ваш опыт преподавания.")
            if not cleaned_data.get("certifications"):
                self.add_error(
                    "certifications",
                    "Укажите ваши сертификаты или квалификации.",
                )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get("role")

        if role == "instructor":
            user.is_instructor = True

        if commit:
            user.save()
            if role == "instructor":
                InstructorProfile.objects.create(
                    user=user,
                    experience=self.cleaned_data.get("experience", ""),
                    certifications=self.cleaned_data.get("certifications", ""),
                )
        return user
