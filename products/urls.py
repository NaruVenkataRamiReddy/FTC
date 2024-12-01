from django.urls import include, re_path 
from . import views

urlpatterns = [
    re_path(r'^$', views.products, name="products"),
    re_path(r'^filters/(?P<typeID>\w{0,50})/$', views.product_filter, name="product_filter"),
    re_path(r'^product-listing$', views.productlisting, name="productlisting"),
    re_path(r'^payment$', views.payment, name="payment"),
    re_path(r'^cart_listing$', views.cart_listing, name="cart_listing"),
    re_path(r'^order-listing$', views.orderlisting, name="orderlisting"),
    re_path(r'^order-items/(?P<orderID>\w{0,50})/$', views.order_items, name="order_items"),
    re_path(r'^order-edit/(?P<orderID>\w{0,50})/$', views.order_edit, name="order_edit"),
    re_path(r'^order-cancel/(?P<orderID>\w{0,50})/$', views.cancel_order, name="cancel_order"),
    re_path(r'^add/', views.add, name="add"),
    re_path(r'^product-details/(?P<productId>\w{0,50})/$', views.product_details, name="product_details"),
    re_path(r'^update/(?P<productId>\w{0,50})/$', views.update, name="update"),
    re_path(r'^cart-delete/(?P<itemId>\w{0,50})/$', views.delete_item, name="delete_item"),
    re_path(r'^delete/(?P<prodId>\w{0,50})/$', views.delete, name="delete"),
    re_path(r'^stock$', views.stock, name="stock"),
    re_path(r'^deletestock/(?P<id>\w{0,50})/$', views.deletestock, name="deletestock"),
    re_path(r'^order$', views.order, name="order"),
    re_path(r'^companylisting$', views.companylisting, name="companylisting"),
    re_path(r'^addcompany$', views.addcompany, name="addcompany"),
    re_path(r'^deletecompany/(?P<id>\w{0,50})/$', views.deletecompany, name="deletecompany"),
]
