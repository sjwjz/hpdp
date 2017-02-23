from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^(?P<task_id>\d+)/$',views.detail),
]