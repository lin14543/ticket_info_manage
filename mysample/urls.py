from django.conf.urls import url

from mysample.apps import MysampleConfig
from . import views
app_name = 'mysample'

urlpatterns = [
    # ex: /mysample/
    url(r'^$', views.index, name='index'),
    url(r'^tables', views.tables, name='tables'),
]