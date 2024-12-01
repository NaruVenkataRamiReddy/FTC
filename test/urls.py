from django.urls import include, re_path 
from . import views

urlpatterns = [
    re_path(r'^$', views.listing, name="listing"),
    re_path(r'^report/(?P<doctorId>\w{0,50})/$', views.listing, name="listing"),
    re_path(r'^add$', views.add, name="add"),
    re_path(r'^update/(?P<testId>\w{0,50})/$', views.update, name="update"),
    re_path(r'^delete/(?P<testId>\w{0,50})/$', views.delete, name="delete"),
]