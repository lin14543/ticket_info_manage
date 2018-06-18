# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
import time
from ticketManage import settings

# Create your models here.


class Tickets(models.Model):
    flightNumber = models.CharField('航班号', max_length=20)
    depTime = models.IntegerField('起始时间')
    arrTime = models.IntegerField('到达时间')
    depAirport = models.CharField('起始机场', max_length=6)
    arrAirport = models.CharField('到达机场', max_length=6)
    currency = models.CharField('货币', max_length=6)
    adultPrice = models.IntegerField('价格', default=0)
    adultTax = models.IntegerField('税价', default=0)
    netFare = models.IntegerField('净票价', default=0)
    maxSeats = models.IntegerField("座位数", default=0)
    cabin = models.CharField('舱位', max_length=10)
    carrier = models.CharField('航司', max_length=5)
    isChange = models.IntegerField('是否中转')
    getTime = models.IntegerField('更新时间')
    addTime = models.IntegerField('添加时间')
    segments = models.TextField('航班信息')
    user = models.ManyToManyField('auth.User', blank=True, null=True)

    def depDatetime(self):
        return time.strftime('%Y-%m-%d %H:%M', time.localtime(self.depTime))

    def arrDatetime(self):
        return time.strftime('%Y-%m-%d %H:%M', time.localtime(self.depTime))

    def getDatetime(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.getTime))

    def __str__(self):
        return self.flightNumber

    class Meta:
        verbose_name = '机票信息'
        verbose_name_plural = '机票信息管理'
        ordering = ['getTime']

    depDatetime.short_description = '出发时间'
    arrDatetime.short_description = '到达时间'

    dep, arr = property(depDatetime), property(arrDatetime)


class Host(models.Model):
    host_name = models.CharField('host_name', max_length=50)
    mem_total = models.CharField('mem_total', max_length=50)
    mem_free = models.CharField('mem_free', max_length=50)
    mem_available = models.CharField('mem_available', max_length=50)
    cpu_Mhz = models.CharField('cpu_Mhz', max_length=50)
    model = models.CharField('model', max_length=50)
    update_time = models.DateTimeField('update_time', auto_now=True)

    def update_datetime(self):
        return self.update_time.strftime('%Y-%m-%d %H:%M:%S')


class Spider(models.Model):
    carrier = models.CharField('carrier', max_length=50)
    host = models.CharField('host', max_length=50)
    num = models.IntegerField('num', default=1)
    last_time = models.DateTimeField('update_time', auto_now=True)
    permins = models.IntegerField('items/min', default=0)

    def last_datetime(self):
        return self.last_time.strftime('%Y-%m-%d %H:%M:%S')


# static==0: 正常运行
# static==1: 暂停状态
# static==3: 还没添加
class Task(models.Model):
    carrier = models.CharField('carrier', max_length=50)
    num = models.IntegerField('host', default=0)
    update_time = models.DateTimeField('update_time', auto_now=True)
    static = models.IntegerField('static', default=0)

    def update_datetime(self):
        return self.update_time.strftime('%Y-%m-%d %H:%M:%S')

    def static_str(self):
        return settings.TASK_STATIC[self.static]



class Concerned(models.Model):
    depAirport = models.CharField('出发机场', max_length=10, null=True)
    arrAirport = models.CharField('到达机场', max_length=10, null=True)
    flightNumber = models.CharField('航班号', max_length=10, null=True)
    ticket = models.ForeignKey(Tickets, blank=True, null=True)
    depTime = models.DateTimeField('出发日期', auto_now=True)
    user = models.ForeignKey('auth.User', blank=True, null=True)

    def __str__(self):
        return self.user

    def get_username(self):
        return self.user.username

    class Meta:
        verbose_name = '特别关注'
        verbose_name_plural = '特别关注管理'

