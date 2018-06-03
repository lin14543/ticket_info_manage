# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
# @login_required


def index(request):
    return render_to_response('index.html')


def tables(request):
    return render_to_response('tables.html')


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
    return render_to_resnse('login.html')


def navbar(request):
    return render_to_response('navbar.html')


def register(request):
    return render_to_response('register.html')


def charts(request):
    return render_to_response('charts.html')


def cards(request):
    return render_to_response('cards.html')


def forgot_password(request):
    return render_to_response('forgot-password.html')