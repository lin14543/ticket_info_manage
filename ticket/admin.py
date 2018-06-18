# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from ticket.models import Tickets, Concerned

# Register your models here.
# admin.site.register(Tickets)


class TicketsAdmin(admin.ModelAdmin):

    list_display = ['flightNumber', 'depAirport', 'arrAirport', 'dep', 'arr', 'adultPrice', 'currency', 'maxSeats']
    list_per_page = 10
    search_fields = ['flightNumber', 'depAirport', 'arrAirport']
    list_filter = ('currency', )

class ConcernedAdmin(admin.ModelAdmin):
    list_display = ['dep']


admin.site.site_header = '航班信息后台管理'
admin.site.site_title = 'Tickets'
admin.site.register(Tickets, TicketsAdmin)
admin.site.register(Concerned)

