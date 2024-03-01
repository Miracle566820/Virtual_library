
# Create your models here.
from django.db import models


class Reader(models.Model):
    username = models.CharField(verbose_name='用户名称', max_length=32)
    major = models.CharField(verbose_name='专业', max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    def __str__(self):
        return self.username


class Book(models.Model):
    book_id = models.CharField(verbose_name='编号', max_length=32,unique=True)
    title = models.CharField(verbose_name='书名', max_length=32)
    author = models.CharField(verbose_name='作者', max_length=32)
    class_name = models.CharField(verbose_name='分类', max_length=32)
    ISBN = models.CharField(verbose_name='条形码', max_length=32)
    publish = models.CharField(verbose_name='出版社', max_length=32)
    borrow_times = models.IntegerField(verbose_name='借阅次数', null=True, blank=True)
    borrow_state_choices = (
        (1, "在馆"),
        (2, "已借出"),
    )
    borrow_state = models.SmallIntegerField(verbose_name="借阅状态", choices=borrow_state_choices)

    def __str__(self):
        return self.title


class Record(models.Model):
    operate_time = models.DateTimeField(verbose_name='记录时间', auto_now_add=True)
    borrow_date = models.DateTimeField(verbose_name='借出时间')
    return_date = models.DateTimeField(verbose_name='归还时间', null=True, blank=True)
    character = models.CharField(verbose_name='属性', max_length=32)
    reader = models.ForeignKey(verbose_name='借阅人', to='Reader', to_field='id', on_delete=models.CASCADE)
    book = models.ForeignKey(verbose_name='书名', to='Book', to_field='id', on_delete=models.CASCADE)
    state_choices = (
        (1, "已归还"),
        (2, "未归还"),
    )
    state = models.SmallIntegerField(verbose_name="状态", choices=state_choices)
