from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):
    return redirect('account_login')

@login_required
def profile(request):
    if (request.user.is_superuser):
        return redirect('admin:index')
    return profileRender(request, {})

def profileRender(request, context):
    return render(request, 'account/profile.html', context)

@login_required
def dashboard(request):
    return dashboardRender(request, {})

def dashboardRender(request, context):
    return render(request, 'dashboard/dashboard.html', context)

