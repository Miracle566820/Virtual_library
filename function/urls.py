"""function URL Configuration

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


from library_python import views
from django.urls import path,include

#一级路由文件
urlpatterns = [
    path('', views.start,name="start"),
    path('choose/',views.choose,name="choose"),
    path('choose/login/',views.login,name="login"),
    path('choose/login/reader', views.login,name="reader"),
    path('choose/login/admin_login', views.admin,name="admin"),
    path('choose/admin_login', views.admin_login,name="admin_operate"),
    path('choose/login/admin_operate', views.admin_operate,name="admin_operate"),
    path('choose/login/reader_operate', views.reader_operate,name="reader_operate"),
    path('choose/login/reader_borrow', views.reader_borrow,name="reader_borrow")

]


