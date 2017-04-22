from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^alice1', views.alice1, name='alice1'),
    url(r'^alice2', views.alice2, name='alice2'),
    url(r'^bob1', views.bob1, name='bob1'),
    url(r'^bob2', views.bob2, name='bob2'),
    ]