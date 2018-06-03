# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import loader
# Create your views here.


def index(request):
    # return HttpResponse('林次次')
    return render_to_response('index.html')


def tables(request):
    return render_to_response('tables.html')


def login(request):
    return render_to_response('login.html')


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

# Create your views here.
