from .reader_operate import rd_opt

class libraray:
    def __init__(self):
        self.reader_statu = 0
        self.manager_statu = 0

    def home(self):
        print("-------借阅者操作------  --------管理员操作-------")
        print("     [1]:查看书籍             [6]:添加书籍\n     [2]:借阅书籍             [7]:删除书籍\n     [3]:归还书籍             [8]:添加读者信息\n     [4]:续借书籍             [9]:删除读者信息\n     [5]:管理员登陆           [10]:查看读者信息\n                              [11]:查看借阅记录\n     [12]:退出")
        choose = input("请输入:")
        if choose == '1':
            self.reader.books_info(self.book_list)
            self.home()

        if choose == '2':
            book_id = input("请输入您要借阅的书籍号:")
            day = input("请输入借阅天数:")
            self.reader.book_borrow(self.book_list, book_id, int(day))
            self.record_list = self.reader.RecordList_init()
            self.home()

        if choose == '3':
            book_id = input("请输入您要归还的书籍号:")
            self.reader.book_return(self.book_list, book_id)
            self.record_list = self.reader.RecordList_init()
            self.home()

        if choose == '4':
            book_id = input("请输入您要续借的书籍号:")
            day = input("请输入续借天数:")
            self.reader.book_continue_borrow(self.book_list, book_id, int(day))
            self.record_list = self.reader.RecordList_init()
            self.home()
        
        if choose == '5':
            key = input('请输入管理员密钥:')
            if key == '888':
                self.manager_statu = 1
                print("已获得管理员权限")
                self.home()
            else:
                print("密钥错误！")
                self.home()

        if choose == '6':
            if self.manager_statu == 1:
                self.reader.db_opt.book_add()
                self.book_list = self.reader.BookList_init()
                self.home()
            else:
                print("抱歉，您没有权限！")

        if choose == '7':
            if self.manager_statu == 1:
                self.reader.db_opt.book_delete()
                self.book_list = self.reader.BookList_init()
                self.home()
            else:
                print("抱歉，您没有权限！")
        
        if choose == '8':
            if self.manager_statu == 1:
                self.reader.db_opt.user_add()
                self.reader_list = self.reader.ReaderList_init()
                self.home()
            else:
                print("抱歉，您没有权限！")

        if choose == '9':
            if self.manager_statu == 1:
                self.reader.db_opt.user_delete()
                self.reader_list = self.reader.ReaderList_init()
                self.home()
            else:
                print("抱歉，您没有权限！")
        
        if choose == '10':
            if self.manager_statu == 1:
                self.reader.readers_info(self.reader_list)
                self.home()
            else:
                print("抱歉，您没有权限！")
        
        if choose == '11':
            if self.manager_statu == 1:
                self.reader.records_info(self.record_list)
                self.home()
            else:
                print("抱歉，您没有权限！")

        if choose == '12':
            print("期待和您的下次见面，祝您阅读愉快，再见！")
            exit(0) 
        
        else:
            self.home()

    def reader_login(self):
        reader_id = input("请输入读者号：")
        self.reader = rd_opt(reader_id)
        if self.reader.db_opt.login_status == 1: #登录成功
            self.reader_statu = 1 
            self.book_list = self.reader.BookList_init()
            self.reader_list = self.reader.ReaderList_init()
            self.record_list = self.reader.RecordList_init()
            self.home()

        else:
            print("登陆失败！")

if __name__ == '__main__':
    libraray_inst = libraray()
    libraray_inst.reader_login()
