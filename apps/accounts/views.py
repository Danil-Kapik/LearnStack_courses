# from django.shortcuts import render, redirect
# from .forms import CustomUserCreationForm
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import login


# def register_view(request):
#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect("courses:home")
#     else:
#         form = CustomUserCreationForm()
#     return render(request, "accounts/register.html", {"form": form})


# def login_view(request):
#     if request.method == "POST":
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect("courses:home")
#     else:
#         form = AuthenticationForm()
#     return render(request, "accounts/login.html", {"form": form})


from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm


def signup(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("courses:home")
    else:
        form = RegistrationForm()
    return render(request, "accounts/signup.html", {"form": form})
