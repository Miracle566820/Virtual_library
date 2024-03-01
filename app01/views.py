from django.shortcuts import render, redirect
from django import forms
from app01.utils.bootstrap import BootStrapForm, BootStrapModelForm
from app01 import models
from django.db.models import Q
import datetime


# Create your views here.


# 初始页面
def start(request):
    return render(request, 'start.html')


# 页面一——————————————登录界面与管理员登录

class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="请输入用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="请输入密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(data=request.POST)
    if form.is_valid():

        reader_object = models.Reader.objects.filter(**form.cleaned_data).first()
        if not reader_object:
            form.add_error("password", "用户名或密码错误")
            # form.add_error("username", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})

        # 用户名和密码正确
        # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；
        request.session["info"] = {'id': reader_object.id, 'name': reader_object.username}
        # session可以保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect("/reader/",{'id': reader_object.id, 'username': reader_object.username})

    return render(request, 'login.html', {'form': form})


def reader(request):
    search_list = ['title__contains', 'author__contains', ]
    search_value = request.GET.get('book_name', '')
    conn = Q()
    conn.connector = 'OR'
    if search_value:
        for item in search_list:
            conn.children.append((item, search_value))

    # 根据搜索条件去数据库获取
    queryset = models.Book.objects.filter(conn)

    return render(request, 'reader.html',{'queryset': queryset})


def admin_login(request):
    return render(request, 'admin_login.html')


# 页面二——————————————选择为用户/管理员界面

def choose(request):
    return render(request, 'choose.html')


# 页面三——————————————用户功能


def reader_borrow(request):
    """用户借阅记录"""
    username = request.session.get('info')['name']
    id = request.session.get('info')['id']
    queryset = models.Record.objects.filter(reader=id)
    return render(request, 'reader_borrow.html', {'queryset': queryset, 'username': username})


def hot_book(request):
    """热门图书"""
    queryset = models.Book.objects.all().order_by('-borrow_times')[0:10]
    return render(request, 'hot_book.html', {'queryset': queryset})


def borrow(request, pk):
    """借书操作按钮"""
    book_object = models.Book.objects.filter(id=pk).first()
    borrow_times = book_object.borrow_times + 1
    models.Book.objects.filter(id=pk).update(borrow_state=2,borrow_times=borrow_times)

    borrow_date = datetime.datetime.now()
    return_date = datetime.datetime.now() + datetime.timedelta(days=7)
    character = '借书'
    reader = request.session.get('info')['id']
    book = pk
    state = 2
    models.Record.objects.create(borrow_date=borrow_date,return_date=return_date,character=character,reader_id=reader,book_id=book,state=state)
    return redirect('/reader/')


def return_book(request, pk):
    """还书操作按钮"""
    models.Book.objects.filter(id=pk).update(borrow_state=1)
    return_date = datetime.datetime.now()
    character = '还书'
    models.Record.objects.filter(book_id=pk).update(state=1,character=character,return_date=return_date)
    return redirect('/reader/reader_borrow/')


def reborrow_book(request, pk):
    """借书操作按钮"""
    book_object = models.Book.objects.filter(id=pk).first()
    borrow_times = book_object.borrow_times + 1
    models.Book.objects.filter(id=pk).update(borrow_state=2,borrow_times=borrow_times)

    borrow_date = datetime.datetime.now()
    return_date = datetime.datetime.now() + datetime.timedelta(days=7)
    character = '续借'
    reader = request.session.get('info')['id']
    book = pk
    state = 2
    models.Record.objects.create(borrow_date=borrow_date,return_date=return_date,character=character,reader_id=reader,book_id=book,state=state)
    return redirect('/reader/reader_borrow/')


def borrow_again(request, pk):
    """用户续借书籍"""
    book_object = models.Book.objects.filter(id=pk).first()
    borrow_times = book_object.borrow_times + 1
    models.Book.objects.filter(id=pk).update(borrow_times=borrow_times)

    return_date = datetime.datetime.now() + datetime.timedelta(days=14)
    book = pk
    models.Record.objects.filter(book_id=book, state=2).update(return_date=return_date)
    return redirect('/reader/reader_borrow/')