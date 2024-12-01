from django.urls import include, re_path 
from . import views

urlpatterns = [
    re_path(r'^$', views.listing, name="company-listing"),
    re_path(r'^list$', views.lists, name="company-lists"),
    re_path(r'^add$', views.add, name="add"),
    re_path(r'^delete/(?P<id>\w{0,50})/$', views.delete, name="delete"),
    re_path(r'^update/(?P<companyId>\w{0,50})/$', views.update, name="update"),
]
