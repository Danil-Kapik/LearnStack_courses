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
