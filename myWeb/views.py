from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
from public.models import UserProfile
from django.contrib.auth.models import AbstractBaseUser


@login_required
def home(request):
    from public.models import Configurations
    config = Configurations.objects.all().first()
    return render(request, 'home.html',locals())


def auth_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get('password')
        user_auth = authenticate(username=username, password=password)
        if user_auth:
            login(request, user_auth)
            return redirect('/home')
        else:
            error_message = 'Email or password is wrong!'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')


@login_required
def auth_logout(request):
    logout(request)
    return redirect('/logout')

@login_required
def lock_account(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get('password')
        user_auth = authenticate(username=username, password=password)
        if user_auth:
            login(request, user_auth)
            return redirect('/home')
        else:
            error_message = '账号或密码错误'
            return render(request, 'lock.html', {'error_message': error_message})
    user = request.user
    return render(request, 'lock.html',locals())


@login_required
def profile(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get('password')
        user_auth = authenticate(username=username, password=password)
        if user_auth:
            login(request, user_auth)
            return redirect('/home')
        else:
            error_message = '账号或密码错误'
            return render(request, 'lock.html', {'error_message': error_message})

    else:
        userinfo = UserProfile.objects.filter(username=str(request.user)).first()
        photo = userinfo.photo
        if photo:photo = "/"+ str(userinfo.photo)
        userinfo.photo = photo
        skills = userinfo.skills
        if skills:skills=skills.split(";")
        userinfo.skills = skills
        return render(request, 'profile.html',locals())

def guid(request):

    return render(request, 'guid.html')

def about(request):
    return render(request, 'about.html')

def register(request):
    return render(request, 'register.html')


def forbidden(request):
    return render(request, '403.html')


def test(request):
    return render(request, 'task.html')
