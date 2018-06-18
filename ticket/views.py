# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from models import Tickets, Host, Task, Spider
import time, traceback, requests, json
from .forms import UserForm
from django.contrib.auth.models import User
from datetime import datetime
from ticketManage import settings

# Create your views here.


def index(request):
    tickets = Tickets.objects.all()
    ticket = tickets[0]
    field_names = ticket._meta.get_all_field_names()
    for name in field_names:
        value = ticket.getattr(name)
        print(name, value)
    return render_to_response('index.html', locals())


def task_info(request):
    try:
        tasks = json.loads(requests.get(settings.GET_STATIC_URL, timeout=60).text).get('data')
        print(tasks)
        update_time = datetime.now()
        for task in tasks:
            carrier=task.get('carrier')
            num = int(task.get('num'))
            static = task.get('static')
            try:
                old = Task.objects.get(carrier=carrier)
                old.num = num
                old.static = static
                old.update_time = update_time
                old.save()
            except:
                new = Task.objects.create(**dict(
                    num=num,
                    carrier=carrier.upper(),
                    static=static,
                    update_time=update_time,
                ))
                new.save()
    except:
        traceback.print_exc()
        # return HttpResponse('GET SPIDER ERROR !!!')
    finally:
        tasks = Task.objects.all()
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return render_to_response('task_info.html', locals())


def add_task(request):
    if request.POST:
        carrier = request.POST.get("carrier")
        operation = request.POST.get("operation")
        ret = {}
        try:
            params = dict(
                carrier=carrier,
            )
            url = r'%s/%s' % (settings.BASE_API_URL, operation)
            print(url)
            res = requests.get(url, params=params, timeout=60).text
            res_dict = json.loads(res)
            print(res)
            if not res_dict.get('status'):
                task = Task.objects.get(carrier=carrier)
                task.static = 0
                task.save()
                ret['status'] = 0
                ret['msg'] = 'success'
        except:
            traceback.print_exc()
            ret['status'] = 1
            ret['msg'] = 'request error'
        finally:
            return HttpResponse(json.dumps(ret))


def operate_host(request):
    if request.POST:
        host = request.POST.get("host")
        operation = request.POST.get("operation")
        url = '%s/%s' % (settings.BASE_API_URL, 'pushcmd')
        key = settings.HOST_KEY.get(operation)
        data = dict(
            cmds=[key],
            devices=[host],
        )
        try:
            print(data)
            res = requests.post(url, data=json.dumps(data), timeout=60)
            print(res.text)
            return HttpResponse(res.text)
        except:
            traceback.print_exc()
            return HttpResponse('RESTART ERROR !!!')



def restart_spider(request):
    if request.POST:
        host = request.POST.get("host")
        print(host)
        carrier = request.POST.get("carrier")
        num = request.POST.get('num')
        key = '%s -a host_name=%s -a num=%s' % (carrier.lower(), host, num)
        url = '%s/%s' % (settings.BASE_API_URL, 'pushcmd')
        cmd = "ps -ef | grep '%s' | grep -v grep | cut -c 9-15 | xargs kill -9" % key
        data = dict(
            cmds=[cmd],
            devices=[host]
        )
        try:
            print(data)
            res = requests.post(url, data=json.dumps(data), timeout=60)
            print(res.text)
            return HttpResponse(res.text)
        except:
            traceback.print_exc()
            return HttpResponse('RESTART ERROR !!!')

@csrf_exempt
def spider_info(request):
    try:
        spiders_dict = json.loads(requests.get(settings.GET_SPIDER_URL, timeout=60).text).get('data')
        for spider_dict in spiders_dict:
            host, carrier, num = spider_dict.get('name').split(":")
            last_time = datetime.fromtimestamp(float(spider_dict.get('last_time'))).strftime('%Y-%m-%d %H:%M:%S')
            permins = spider_dict.get('permins')
            spider = dict(
                host=host,
                carrier=carrier.upper(),
                num=num,
                permins=permins,
                last_time=last_time,
            )
            try:
                spider = Spider.objects.get(host=host, carrier=carrier, num=num)
                spider.last_time = last_time
                spider.permins = permins
                spider.save()
            except:
                spider = Spider.objects.create(**spider)
                spider.save()
    except:
        traceback.print_exc()
        # return HttpResponse('GET SPIDER ERROR !!!')
    finally:
        now_time = time.strftime('%Y-%m-%d %H:%M:%S')
        spiders = Spider.objects.all()
        return render_to_response('spider-info.html', locals())


def tables(request):
    tickets = Tickets.objects.all()
    for ticket in tickets:
        print(ticket.user)
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return render_to_response('tables.html', locals())


@login_required
def concerned(request):
    user = User.objects.get(username=request.session.get('username'))
    tickets = user.tickets_set.all()
    for ticket in tickets:
        print(ticket.depTime)
        print(ticket.arrTime)
        print(ticket.flightNumber)
    return render_to_response('concerned.html', locals())


def host_info(request):
    hosts = Host.objects.all()
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return render_to_response('host-info.html', locals())



@login_required
def add_concern(request):
    if request.POST:
        id = request.POST.get("ticket_id")
        ticket = Tickets.objects.get(id=id)
        user_name = request.session.get("username")
        user = User.objects.get(username=user_name)
        ticket.user.add(user)
        return HttpResponse({'msg', 'success'})
    return HttpResponse("request error")


def delete_concern(request):
    if request.POST:
        id = request.POST.get("ticket_id")
        ticket = Tickets.objects.get(id=id)
        user_name = request.session.get('username')
        user = User.objects.get(username=user_name)
        ticket.user.remove(user)
        user = User.objects.get(username=request.session.get('username'))
        tickets = user.tickets_set.all()
        a = {'a': 'b'}
        return json.dumps(a)
    return HttpResponse("request error")


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
                request.session['username'] = username
                return redirect('/')
            msg = '该用户无权登录'
        else:
            msg = '用户名或密码错误.'
        return render_to_response('login.html', {'error_msg': msg})
    return render_to_response('login.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect('/')


def navbar(request):
    return render_to_response('navbar.html')


@csrf_exempt
def register(request):
    if request.POST:
        print('post')
        form = UserForm(request.POST)
        if form.is_valid():
            print('True')
            password = form.cleaned_data['password']
            cpassword = form.cleaned_data['confirmpassword']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            error_msg = []
            if password != cpassword:
                error_msg.append('两次密码不一致')
            user = authenticate(username=username, pword=password)
            if user:
                error_msg.append('该用户名已被注册')
            if len(error_msg):
                return render(request, 'register.html', locals())
            user_dict = dict(
                username=username,
                password=password,
                email=email,
                date_joined=datetime.now(),
                last_login=datetime.now(),
            )
            user = User.objects.create_user(**user_dict)
            user.save()

            login(request, user)
            return redirect('/', locals())
    return render(request, 'register.html', {'anser': locals()})
    # return render_to_response('register.html', {'anser': locals()}, context_instance=RequestContext(request))


def charts(request):
    return render_to_response('charts.html')


def cards(request):
    return render_to_response('cards.html')


def forgot_password(request):
    return render_to_response('forgot-password.html')