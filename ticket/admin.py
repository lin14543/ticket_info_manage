# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from ticket.models import Tickets, Concerned

# Register your models here.
admin.site.register(Tickets)
admin.site.register(Concerned)

