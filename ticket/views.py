# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from models import Tickets
import time

# Create your views here.
# @login_required


def index(request):

    tickets = Tickets.objects.all()
    return render_to_response('index.html', locals())


def tables(request):
    tickets = Tickets.objects.all()
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return render_to_response('tables.html', locals())


@csrf_exempt
def login_user(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            print(username)
            if user.is_active:
                login(request, user)
                return redirect('/')
            msg = '该用户无权登录'
        else:
            msg = '用户名或密码错误.'
        return render_to_response('login.html', {'error_msg': msg})
    return render_to_response('login.html')


@login_required
def logout_user(request):
    logout(request)
    print('haha')
    return redirect('/')


def navbar(request):
    return render_to_response('navbar.html')


def register(request):
    if request.POST:
        password = request.POST.get('password')
        cpassword = request.POST.get('confirmpassword')
        username = request.POST.get('username')
        email = request.POST.get('email')
        if password != cpassword:
            msg = '两次密码不一致，请重新输入'
            return render_to_response('register.html', locals())

    return render_to_response('register.html')


def charts(request):
    return render_to_response('charts.html')


def cards(request):
    return render_to_response('cards.html')


def forgot_password(request):
    return render_to_response('forgot-password.html')