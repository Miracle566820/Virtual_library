
# Create your models here.
from django.db import models
import pymysql
class Reader_Node:
    def __init__(self):
        self.reader_id = 0
        self.name = ''
        self.major = ''
        self.password = ''


class Record_Node:
    def __init__(self):
        self.operate_id = 0
        self.operate_time = ''
        self.character = ''
        self.reader_id = ''
        self.reader_name = ''
        self.book_id = ''
        self.book_name = ''
        self.borrow_date = ''
        self.return_date = ''
        self.state = ''



class db_opt:
    def __init__(self):
        self.db = pymysql.connect(host='localhost',  
                        user='root',
                        password='123456',
                        database='libraray',
                        charset='utf8')
        self.cursor = self.db.cursor()
        self.login_status = 0

    def login(self, reader_id):
        sql = "SELECT reader_id,name,major,password FROM readers WHERE reader_id='%s'" %(reader_id)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        # print(result)
        # 判断用户表里有没有输入的读者号
        if result:
            res = result[0]
            print("%s登陆中......" %(res[1]))
            password = str(input("请输入你的借阅密码："))
            if password == str(res[3]):
                print("登陆成功！欢迎进入SHU图书借阅系统！")
                self.login_status = 1
                return self.login_status, res[1]
            else:
                print("密码错误，请重试！")
                self.login_status = 0
                return self.login_status, ''
        else:
            print("用户不存在，请联系管理员注册！")
            login_status = 0
            return login_status, ''