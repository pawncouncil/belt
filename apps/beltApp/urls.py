from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),

    url(r'^main$', views.main),
    url(r'^add$', views.add),
    url(r'^createTrip$', views.createTrip),
    url(r'^join/(?P<trip_id>\d+)$', views.join),
    url(r'^destination/(?P<trip_id>\d+)$', views.destination),
    url(r'^remove/(?P<trip_id>\d+)$', views.remove),
    url(r'^delete/(?P<trip_id>\d+)$', views.delete)
]