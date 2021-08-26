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
    return render(request, 'common/home.html', locals())


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
            return render(request, 'common/login.html', {'error_message': error_message})
    return render(request, 'common/login.html')


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
            return render(request, 'common/lock.html', {'error_message': error_message})
    user = request.user
    return render(request, 'common/lock.html', locals())


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
            return render(request, 'common/lock.html', {'error_message': error_message})

    else:
        userinfo = UserProfile.objects.filter(username=str(request.user)).first()
        photo = userinfo.photo
        if photo: photo = "/" + str(userinfo.photo)
        userinfo.photo = photo
        skills = userinfo.skills
        if skills: skills = skills.split(";")
        userinfo.skills = skills
        return render(request, 'common/profile.html', locals())


def guid(request):
    return render(request, 'common/guid.html')


def about(request):
    return render(request, 'common/about.html')


def register(request):
    return render(request, 'common/register.html')


def test(request):
    return render(request, 'task.html')


def page_not_found(request,exception):
    return render(request, 'error/404.html')


def internal_error(request):
    return render(request, 'error/500.html')
