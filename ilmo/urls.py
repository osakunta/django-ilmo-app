from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^events/all/$',views.get_all_events),
    url(r'^events/coming/$',views.get_coming_events),
    url(r'^event/(\d+)/$',views.parse_event_form),
    url(r'^event/\d+/register/$',views.thanks)
]
