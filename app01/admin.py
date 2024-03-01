from django.contrib import admin
from app01.models import Reader, Record, Book


# Register your models here.

class ReaderAdmin(admin.ModelAdmin):
    list_display = ('username', 'major')  # list


class RecordAdmin(admin.ModelAdmin):
    list_display = ('operate_time', 'borrow_date', 'return_date', "character", 'reader', 'book', 'state')  # list


class BookAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'title', 'author', 'class_name', 'ISBN', 'publish', 'borrow_times', 'borrow_state')  # list


admin.site.register(Record, RecordAdmin)
admin.site.register(Reader, ReaderAdmin)
admin.site.register(Book, BookAdmin)

admin.site.site_title = '图书馆后台管理系统'
admin.site.site_header = '欢迎使用图书馆后台管理系统'
