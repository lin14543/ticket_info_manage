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
    url(r'logout/$', views.logout_user, name='logout'),
]