from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^events/$',views.get_all_events)
]
