from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ProfileForm, LeaveForm, ComplaintForm
from .models import Profile

def home(request):
    return render(request, "main/home.html")

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        Profile.objects.create(user=user)
        return redirect("login")
    return render(request, "main/register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        u = request.POST["username"]
        p = request.POST["password"]
        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            return redirect("home")
        messages.error(request, "Invalid credentials")
    return render(request, "main/login.html")

@login_required
def user_logout(request):
    logout(request)
    return redirect("login")

@login_required
def change_password(request):
    if request.method == "POST":
        old = request.POST["old_password"]
        new = request.POST["new_password"]
        if request.user.check_password(old):
            request.user.set_password(new)
            request.user.save()
            messages.success(request, "Password changed. Please log in again.")
            return redirect("login")
        messages.error(request, "Wrong old password")
    return render(request, "main/change_password.html")

@login_required
def profile(request):
    prof = request.user.profile
    form = ProfileForm(request.POST or None, instance=prof)
    if form.is_valid():
        form.save()
        messages.success(request, "Profile updated")
    return render(request, "main/profile.html", {"form": form})

@login_required
def leave_request(request):
    form = LeaveForm(request.POST or None)
    if form.is_valid():
        leave = form.save(commit=False)
        leave.user = request.user
        leave.save()
        messages.success(request, "Leave submitted")
        return redirect("home")
    return render(request, "main/leave.html", {"form": form})

@login_required
def file_complaint(request):
    form = ComplaintForm(request.POST or None)
    if form.is_valid():
        comp = form.save(commit=False)
        comp.user = request.user
        comp.save()
        messages.success(request, "Complaint submitted")
        return redirect("home")
    return render(request, "main/complaint.html", {"form": form})
