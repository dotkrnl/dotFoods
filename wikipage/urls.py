from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<url_name>[^/]*)/$', views.show, name='show'),
]
