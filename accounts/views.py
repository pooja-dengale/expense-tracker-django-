"""
Views for user authentication.
Handles user registration, login, and logout.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from .forms import RegisterForm, LoginForm


@require_http_methods(["GET", "POST"])
def register_view(request):
    """
    User registration view.
    Allows new users to create an account with username, email, and password.
    GET: Shows registration form
    POST: Processes registration form and creates new user
    """
    if request.user.is_authenticated:
        return redirect('expenses:dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('accounts:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    User login view.
    Authenticates user with username and password.
    GET: Shows login form
    POST: Processes login form and authenticates user
    """
    if request.user.is_authenticated:
        return redirect('expenses:dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('expenses:dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@require_http_methods(["POST"])
@login_required
def logout_view(request):
    """
    User logout view.
    Logs out the current user and redirects to home page.
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')
