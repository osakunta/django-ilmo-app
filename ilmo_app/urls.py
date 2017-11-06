from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.get_coming_events),
    url(r'^(.+)/$', views.parse_event_form)
]
