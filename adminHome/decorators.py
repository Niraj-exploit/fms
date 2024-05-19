from functools import wraps
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.is_staff):
            return redirect('login')  # Redirect to login page
        return view_func(request, *args, **kwargs)
    return staff_member_required(wrapper)
