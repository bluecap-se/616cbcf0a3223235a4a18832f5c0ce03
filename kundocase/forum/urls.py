from django.conf.urls import url
from kundocase.forum import views


app_name = 'forum'

urlpatterns = [
    url(r'^$', views.startpage, name='startpage'),
    url(r'^question/?$', views.question, name='new-question'),
    url(r'^question/(?P<id>\d+)$', views.question, name='question'),
    url(r'^answer/?$', views.answer, name='new-answer'),
    url(r'^answer/(?P<id>\d+)/?$', views.answer, name='answer'),
]
