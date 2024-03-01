"""new URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path as url
from django.urls import path
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.start, name="start"),
    path('choose/', views.choose, name="choose"),
    path('choose/login/', views.login, name="login"),
    path('reader/', views.reader, name="reader"),
    path('reader/reader_borrow/', views.reader_borrow,name="reader_borrow"),
    path('hot/book/', views.hot_book,name="hot_book"),
    url(r'^borrow/(?P<pk>\d+)/$', views.borrow,name="borrow_book"),
    url(r'^return/(?P<pk>\d+)/$', views.return_book,name="return_book"),
    url(r'^borrow/again/(?P<pk>\d+)/$', views.borrow_again, name="borrow_again"),


]
