from django.conf.urls import url
from kundocase.forum import views


app_name = 'forum'

urlpatterns = [
    url(r'^$', views.startpage, name='startpage'),
    url(r'^(?P<id>\d+)$', views.question, name='question'),
    url(r'^save-question/?$', views.save_question, name='save-question'),
]
