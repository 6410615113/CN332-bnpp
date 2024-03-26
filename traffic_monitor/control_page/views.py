from django.shortcuts import render, redirect

# Create your views here.
def login(request):
    return redirect('account_login')

def profile(request):
    return profileRender(request, {})

def profileRender(request, context):
    return render(request, 'account/profile.html', context)