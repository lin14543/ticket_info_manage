# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
import time

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
    # fromCity = models.CharField('出发城市', max_length=10)
    # toCity = models.CharField('到达城市', max_length=10)
    segments = models.TextField('航班信息')
    site = models.CharField('站点', null=True, max_length=256)

    def depDatetime(self):
        return time.strftime('%Y-%m-%d %H:%M', time.localtime(self.depTime))

    def arrDatetime(self):
        return time.strftime('%Y-%m-%d %H:%M', time.localtime(self.depTime))

    def __str__(self):
        return self.flightNumber

    class Meta:
        verbose_name = '机票信息'
        verbose_name_plural = '机票信息管理'
        ordering = ['getTime']

    depDatetime.short_description = '出发时间'
    arrDatetime.short_description = '到达时间'

    dep, arr = property(depDatetime), property(arrDatetime)

class Concerned(models.Model):
    depAirport = models.CharField('出发机场', max_length=10)
    arrAirport = models.CharField('到达机场', max_length=10)
    user = models.ForeignKey('auth.User', blank=True, null=True, verbose_name='用户')
    startTime = models.DateTimeField('起始时间', auto_now=True)
    endTime = models.DateTimeField('结束时间', auto_now=True)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = '特别关注'
        verbose_name_plural = '特别关注管理'

