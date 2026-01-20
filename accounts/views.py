from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout


# Create your views here.
def register(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect("login")
    else:
        user_form = UserCreationForm()
    return render(request, "register.html", context={"user_form": user_form})


def login(request):
    if request.method == "POST":
        auth_form = AuthenticationForm(data=request.POST)
        if auth_form.is_valid():
            username = auth_form.cleaned_data.get("username")
            password = auth_form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("cars_list")
            else:
                auth_form = AuthenticationForm()
    else:
        auth_form = AuthenticationForm()

    return render(request, "login.html", context={"auth_form": auth_form})


def logout_view(request):
    logout(request)
    return redirect("cars_list")
