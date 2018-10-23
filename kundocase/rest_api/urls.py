from django.conf.urls import url
from kundocase.rest_api import views


app_name = 'rest_api'

urlpatterns = [
    url(r'^question/?$', views.question, name='questions'),
    url(r'^question/(?P<id>\d+)/?$', views.question, name='question'),
    url(r'^question/(?P<qid>\d+)/answer/?$', views.answer, name='answers'),
    url(r'^question/(?P<qid>\d+)/answer/(?P<aid>\d+)/?$', views.answer, name='answer'),
]
