# middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test

def admin_required(function=None, redirect_field_name=None, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.groups.filter(name='responsable').exists(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def admin_required_middleware(get_response):
    def middleware(request):
        if request.path == '/crud/' and not request.user.is_authenticated:
            return redirect(reverse('login'))
        if request.path == '/crud/' and not request.user.groups.filter(name='responsable').exists():
            return redirect(reverse('login'))
        return get_response(request)
    return middleware
