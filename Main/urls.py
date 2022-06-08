from django.urls import path, re_path
from django.contrib.auth import views as authViews
from django.views.i18n import JavaScriptCatalog

from .views import *





urlpatterns = [
    path('', Index.as_view(), name="home"),
    path('test_1', Testing.as_view(), name="test_1"),
    path('About', About.as_view(), name="About"),
    path('login', LoginUser.as_view(), name="login"),
    path('register', RegisterUser.as_view(), name="register"),
    path('Cart', CartView.as_view(), name="Cart"),
    path('add_goods', add_goods.as_view(), name="add_goods"),
    path('view_orders', view_orders.as_view(), name="view_orders"),
    path('logout', logout_user, name='logout'),
    re_path(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog')
]
