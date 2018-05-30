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

# Create your views here.
