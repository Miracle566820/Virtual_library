import pymysql
from .tools import generate_book_id, generate_operate_id

from pymysql import NULL
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
                print("登陆成功！\n欢迎进入SHU图书借阅系统！")
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

    def login2(self,reader_id,password):
        sql = "SELECT reader_id,name,major,password FROM readers WHERE reader_id='%s'" %(reader_id)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        # print(result)
        # 判断用户表里有没有输入的读者号
        if result:
            res = result[0]
            print("%s登陆中......" %(res[1]))
            password = str(password)
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
            login_status = -1
            return login_status, ''


    # print(login(20120575))

    def user_add(self):  # 之后做前端可以加个权限
        reader_id = input("请输入您要添加的读者号：")
        name = input("请输入添加人用户的姓名：")
        major = input("请输入添加用户的专业：")
        password = input("请设置添加用户的密码：")
        sql_1 = "INSERT INTO readers VALUES('%s', '%s', '%s', '%s')" %(reader_id, name, major, password)
        self.cursor.execute(sql_1)
        self.db.commit()
        sql_2 = "SELECT reader_id,name,major,password FROM readers WHERE reader_id='%s'" %(reader_id)
        self.cursor.execute(sql_2)
        result = self.cursor.fetchone()
        if result:
            print("添加成功！")
            add_status = 1
            return add_status
        else:
            print("添加失败")
            add_status = 0
            return add_status
    
    def user_delete(self):
        reader_id = input("请输入您要删除的读者号：")
        sql_1 = "SELECT reader_id FROM readers WHERE reader_id='%s'" %(reader_id)
        self.cursor.execute(sql_1)
        result = self.cursor.fetchall()
        if result:
            sql_2 = "DELETE FROM `libraray`.`readers` WHERE (`reader_id` = '%s')" %(reader_id)
            self.cursor.execute(sql_2)
            self.db.commit()
            print("删除成功！")
            delete_status = 1
            return delete_status
        else:
            print("用户库里没有该用户，删除失败！")
            delete_status = 0
            return delete_status

    def book_add(self):
        book_id = generate_book_id()
        name = input("请输入您要添加的书名：")
        author = input("请输入添加书的作者：")
        class_name = input("请输入书的性质：")
        ISBN = input("请输入ISBN：")
        publish = input("请输入出版社：")
        borrow_state = input("请输入借出状态：")
        borrow_times = '0'
        sql_1 = "INSERT INTO books VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s')" %(book_id, name, author, class_name,ISBN, publish, borrow_state,'','',borrow_times)
        self.cursor.execute(sql_1)
        self.db.commit()
        sql_2 = "SELECT book_id FROM books WHERE book_id='%s'" %(book_id)
        self.cursor.execute(sql_2)
        result = self.cursor.fetchone()
        if result:
            print("添加成功！")
            add_status = 1
            return add_status
        else:
            print("添加失败")
            add_status = 0
            return add_status

    def book_delete(self):
        book_id = input("请输入您要删除的图书序号：")
        sql_1 = "SELECT book_id FROM books WHERE book_id='%s'" %(book_id)
        self.cursor.execute(sql_1)
        result = self.cursor.fetchall()
        if result:
            sql_2 = "DELETE FROM `libraray`.`books` WHERE (`book_id` = '%d')" %(str(book_id))
            self.cursor.execute(sql_2)
            self.db.commit()
            print("删除成功！")
            delete_status = 1
            return delete_status
        else:
            print("没有该图书，删除失败！")
            delete_status = 0
            return delete_status
    
    def borrow_state_change(self, book_id, borrow_date=' ', return_date=' ', borrow_times= ' ', if_continue_borrow = False):
        sql_1 = "SELECT borrow_state FROM books WHERE book_id='%s'" %(book_id)
        self.cursor.execute(sql_1)
        result = self.cursor.fetchall()
        if result[0][0] == '未借出':
            sql_2 = "UPDATE `libraray`.`books` SET `borrow_state` = '已借出' WHERE (`book_id` = '%s')" %(book_id)
            self.cursor.execute(sql_2)
            self.db.commit()
            sql_3 = "UPDATE `libraray`.`books` SET `borrow_date` = '%s', `return_date` = '%s', `borrow_times` = '%s' WHERE (`book_id` = '%s')" %(borrow_date, return_date, borrow_times, book_id)
            self.cursor.execute(sql_3)
            self.db.commit()
            print("状态修改为已借出")
            return True
        elif result[0][0] == '已借出':
            if if_continue_borrow == False:
                sql_2 = "UPDATE `libraray`.`books` SET `borrow_state` = '未借出' WHERE (`book_id` = '%s')" %(book_id)
                self.cursor.execute(sql_2)
                self.db.commit()
                print("状态修改为未借出")
            sql_3 = "UPDATE `libraray`.`books` SET `borrow_date` = '%s', `return_date` = '%s' WHERE (`book_id` = '%s')" %(borrow_date, return_date, book_id)
            self.cursor.execute(sql_3)
            self.db.commit()
            return True
    
    def record_add(self, operate_time, character, reader_id, reader_name, book_id, book_name, borrow_date, return_date, state):
        operate_id = generate_operate_id()
        sql_1 = "INSERT INTO records VALUES('%s','%s','%s','%s', '%s', '%s', '%s', '%s', '%s','%s')" %(operate_id, operate_time,character, reader_id, reader_name, book_id, book_name, borrow_date, return_date, state)
        self.cursor.execute(sql_1)
        self.db.commit()
        print("数据库记录添加成功！")
        return True

