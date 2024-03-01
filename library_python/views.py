# _*_ encoding:utf-8 _*_
from django.shortcuts import render,redirect
from .library_main import libraray
from .reader_operate import rd_opt
from .mysql_operate import db_opt

#初始页面
def start(request):
    return render(request,'start.html')

#页面一——————————————登录界面与管理员登录

def login(request):
    a = db_opt()
    if request.method == 'POST':
    #判断读者号是否存在，对应密码是否正确
        login_status,reader_name = a.login2(request.POST.get('reader_id'),request.POST.get('password'))
        if login_status == 1:
            return render(request,'reader.html',{'reader_id':reader_name,'status':login_status})
        elif login_status == 0:
            hint=str("账号密码错误")
            return render(request,'login.html',{'status':login_status})
        elif login_status == -1:
            hint=str("账号密码错误")
            return render(request,'login.html',{'status':login_status})
    else:
        return render(request,'login.html')

def admin_login(request):
    a = db_opt()
    if request.method == 'POST':
    #判断读者号是否存在，对应密码是否正确
        admin_login_password = str(request.POST.get('password'))
        if admin_login_password == str(888):
            return render(request,'admin.html')
        else:
            return render(request,'mistake.html')  
    else:
        return render(request,'admin_login.html')
#页面二——————————————选择为用户/管理员界面

def choose(request):
    return render(request,'choose.html')
def reader(request):
    return render(request,'reader.html')
def admin(request):
    return render(request,'admin.html')
    
#页面三——————————————用户功能

def reader_operate(request):
    return render(request,'reader_operate.html')

def reader_borrow(request):
    return render(request,'reader_borrow.html')


def admin_operate(request):
    return render(request,'admin_operate.html')



    