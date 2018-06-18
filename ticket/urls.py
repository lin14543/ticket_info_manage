from django.conf.urls import url

from mysample.apps import MysampleConfig
from . import views
app_name = 'ticket'

urlpatterns = [
    url(r'^$', views.tables, name='index'),
    url(r'^tables', views.tables, name='tables'),
    url(r'^login', views.login_user, name='login'),
    url(r'^index', views.index),
    url(r'^navbar', views.navbar, name='navbar'),
    url(r'^register', views.register, name='register'),
    url(r'^charts', views.charts, name='charts'),
    url(r'^cards', views.cards, name='cards'),
    url(r'^forgot-password', views.forgot_password, name='forgot_password'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^host-info', views.host_info, name='host_info'),
    url(r'^addconcern', views.add_concern, name='add_concern'),
    url(r'^deleteconcern', views.delete_concern, name='delete_concern'),
    url(r'^concerned', views.concerned, name='concerned'),
    url(r'^spider-info', views.spider_info, name='spider_info'),
    url(r'^task-info', views.task_info, name='task_info'),
    url(r'^addtask', views.add_task, name='add_task'),
    url(r'^restart-spider', views.restart_spider, name='restart_spider'),
    url(r'^operatehost', views.operate_host, name='operate_host'),
]