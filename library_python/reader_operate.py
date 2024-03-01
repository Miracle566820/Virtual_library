from pymysql import NULL
from .book_node import Book_Node
from .reader_node import Reader_Node
from .record_node import Record_Node
from .mysql_operate import db_opt
from .tools import date_compare
import datetime
import re


class rd_opt:
    def __init__(self, reader_id):
        self.reader_id = reader_id
        self.db_opt = db_opt()
        _ ,self.name = self.db_opt.login(reader_id)
    
    def BookList_init(self):
        BookList = []
        sql_1 = "select * from books"
        self.db_opt.cursor.execute(sql_1)
        result = self.db_opt.cursor.fetchall()
        book_num = self.db_opt.cursor.execute("SELECT * FROM books")
        for i in range(0, book_num):
            node = Book_Node()
            node.book_id = result[i][0]
            node.name = result[i][1]
            node.author = result[i][2]
            node.class_name = result[i][3]
            node.ISBN = result[i][4]
            node.publish = result[i][5]
            node.borrow_state = result[i][6]
            node.borrow_date = result[i][7]
            node.return_date = result[i][8]
            node.borrow_times = result[i][9]
            BookList.append(node)
        # for i in range(0, book_num):
        #     print(BookList[i].author)
        return BookList
    
    def ReaderList_init(self):
        ReaderList = []
        sql_1 = 'select * from readers'
        self.db_opt.cursor.execute(sql_1)
        result = self.db_opt.cursor.fetchall()
        reader_num = self.db_opt.cursor.execute("SELECT * FROM readers")
        for i in range(0, reader_num):
            node = Reader_Node()
            node.reader_id = result[i][0]
            node.name = result[i][1]
            node.major = result[i][2]
            ReaderList.append(node)
        return ReaderList

    def RecordList_init(self):
        RecordList = []
        sql_1 = "select * from records"
        self.db_opt.cursor.execute(sql_1)
        result = self.db_opt.cursor.fetchall()
        record_num = self.db_opt.cursor.execute("SELECT * FROM records")
        for i in range(0, record_num):
            node = Record_Node()
            node.operate_id = result[i][0]
            node.operate_time = result[i][1]
            node.character = result[i][2]
            node.reader_id = result[i][3]
            node.reader_name = result[i][4]
            node.book_id = result[i][5]
            node.book_name = result[i][6]
            node.borrow_date = result[i][7]
            node.return_date = result[i][8]
            node.state = result[i][9]
            RecordList.append(node)
        return RecordList

    def book_bubble_sort(self, BookList, key):
        """
        冒泡排序
        """
        length = len(BookList)
        if length <= 1:
            return BookList
        for i in range(0, length):
            for j in range (0, length-i-1):
                if BookList[j].__dict__[key] > BookList[j+1].__dict__[key]:
                    (BookList[j], BookList[j+1]) = (BookList[j+1], BookList[j])
        return BookList

    def book_insert_sort(self, BookList, key):
        """
        插入排序
        """
        length = len(BookList)
        if length <= 1:
            return BookList
        for i in range (1,length):
            j = i
            target = BookList[i]
            while (j>0) and (target.__dict__[key] < BookList[j-1].__dict__[key] ):
                BookList[j] = BookList[j-1]
                j = j-1
            BookList[j] = target
        return BookList

    def book_shell_sort(self, BookList, key):
        '''
        希尔排序(插入排序的高效实现)
        '''
        def shellinsert(list, d):
            length = len(list)
            for i in range(d,length):
                j = i-d
                temp = list[i]
                while (j>=0 and list[j].__dict__[key] > temp.__dict__[key]):
                    list[j+d] = list[j]
                    j = j-d
                if j != i-d:
                    list[j+d] = temp
        length = len(BookList)
        if length <= 1:
            return BookList
        d = length // 2
        while d >= 1:
            shellinsert(BookList, d)
            d = d //2
        return BookList




    def book_find(self, BookList, key, value):
        find_result = []
        if key  not in ["book_id", "name", "author", "class_name", "ISBN", "publish", "borrow_state", "borrow_date", "return_date", "borrow_times"]:
            print("没有该属性")
            return find_result
        find_times = 0
        length = len(BookList)
        BookList = self.book_shell_sort(BookList, key)
        '''
        顺序查找
        for i in range(0, len(BookList)):
            find_times = find_times + 1
            if BookList[i].__dict__[key] == value:
                find_result.append(BookList[i])
        '''
        # 二分查找(改良版)
        first = 0
        last = length - 1
        while first <= last:
            mid = (first + last) // 2
            find_times += 1
            if BookList[mid].__dict__[key] > value:
                last = mid - 1
            elif BookList[mid].__dict__[key] < value:
                first = mid + 1
            else:
                find_result.append(BookList[mid])
                k = 1
                q = 1
                while(( (k + mid) <= last ) and BookList[mid+k].__dict__[key] == value):
                    find_times += 1
                    find_result.append(BookList[mid+k])
                    k += 1 
                while(( (mid - q) >= first ) and BookList[mid-q].__dict__[key] == value):
                    find_times += 1
                    find_result.append(BookList[mid-q])
                    q += 1
                break
        print("查找了{}次".format(find_times))
        return find_result
    
    def book_find_new(self, BookList, value):
        find_result = []
        pattern = '.*%s.*'%(value) 
        regex = re.compile(pattern) # 编译正则表达式
        for book in BookList:
            match = ( regex.search(book.name) ) or ( regex.search(book.author) ) or ( regex.search(book.book_id) ) or ( regex.search(book.class_name) ) or ( regex.search(book.ISBN) ) or ( regex.search(book.publish) )
            if match:
                find_result.append(book)
        return find_result

    def book_if_borrowed(self, booknode):
        if booknode.borrow_state == '已借出':
            return True        
        elif booknode.borrow_state == '未借出':
            return False
        else:
            return NULL
    
    def books_info(self, BookList):
        print("ID       书名        作者        类型        ISBN        出版社      借阅状态      借出日期        归还(应还)日期        借阅次数")
        for i in range(0, len(BookList)):
            print(BookList[i].book_id,"   ",
                  BookList[i].name,"   ",
                  BookList[i].author,"   ",
                  BookList[i].class_name,"   ",
                  BookList[i].ISBN,"   ",
                  BookList[i].publish,"   ",
                  BookList[i].borrow_state,"   ",
                  BookList[i].borrow_date,"   ",
                  BookList[i].return_date,"   ",
                  BookList[i].borrow_times,"   "

                  )

    def readers_info(self, ReaderList):
        print("ID       姓名        专业")
        for i in range(0, len(ReaderList)):
            print(ReaderList[i].reader_id,"   ",
                  ReaderList[i].name,"   ",
                  ReaderList[i].major,"   ",
                  )

    def records_info(self, RecordList):
        print("操作ID       操作时间        属性        读者ID      读者姓名        书籍ID      书籍名      借阅时间        (应)归还时间        状态")
        for i in range(0, len(RecordList)):
            print(RecordList[i].operate_id,"   ",
                  RecordList[i].operate_time,"   ",
                  RecordList[i].character,"   ",
                  RecordList[i].reader_id,"   ",
                  RecordList[i].reader_name,"   ",
                  RecordList[i].book_id,"   ",
                  RecordList[i].book_name,"   ",
                  RecordList[i].borrow_date,"   ",
                  RecordList[i].return_date,"   ",
                  RecordList[i].state,"   ",
                  )
    def records_info2(self, RecordList):
        print("操作ID       操作时间        属性        读者ID      读者姓名        书籍ID      书籍名      借阅时间        (应)归还时间        状态")
        for i in range(0, len(RecordList)):
            return (
                  RecordList[i].reader_name,"   ",
                  RecordList[i].book_name,"   ",
                  RecordList[i].borrow_date,"   ",
                  RecordList[i].return_date,"   ",
                  RecordList[i].state,"   ",)

    
    def book_borrow(self, BookList, book_id, day):
        find_result = self.book_find(BookList, 'book_id', book_id)
        if find_result:
            if self.book_if_borrowed(find_result[0]) == True:
                print("抱歉，书籍已经被借出！")
                return False
            elif self.book_if_borrowed(find_result[0]) == False:
                now=datetime.datetime.now()
                now_str = now.strftime('%Y-%m-%d %H:%M:%S')
                # 计算day天后的日期
                delta = datetime.timedelta(days=day)
                future = now + delta
                future_str = future.strftime('%Y-%m-%d %H:%M:%S')
                print("成功借出！")
                # 写入数据
                find_result[0].borrow_state = "已借出"
                find_result[0].borrow_date = now_str
                find_result[0].return_date = future_str
                find_result[0].borrow_times = str(int(find_result[0].borrow_times) + 1)
                self.db_opt.borrow_state_change(book_id, now_str, future_str, borrow_times = find_result[0].borrow_times)
                self.db_opt.record_add(now_str, '借阅', self.reader_id, self.name, book_id, find_result[0].name, now_str, future_str, '正常')
                return True
        else:
            print("数据库里没有这本书！")
            return False

    def book_return(self, BookList, book_id):
        find_result = self.book_find(BookList, 'book_id', book_id)
        if find_result:
            if self.book_if_borrowed(find_result[0]) == True:
                now=datetime.datetime.now()
                now_str = now.strftime('%Y-%m-%d %H:%M:%S')
                # 写入数据
                borrow_date = find_result[0].borrow_date # 记录下之前借的日期
                original_return_date = find_result[0].return_date # 记录下之前应归还的日期
                state = ''
                if date_compare(now_str.split()[0], original_return_date.split()[0]) > 0:
                    state = '逾期'
                    print("成功归还，已逾期！")
                elif date_compare(now_str.split()[0], original_return_date.split()[0]) <= 0:
                    state = '未逾期'
                    print("成功归还，未逾期")
                find_result[0].borrow_state = '未借出'
                find_result[0].borrow_date = ' '
                find_result[0].return_date = ' '
                self.db_opt.borrow_state_change(book_id)
                self.db_opt.record_add(now_str, '归还', self.reader_id, self.name, book_id, find_result[0].name, borrow_date, now_str, state)
                return True
            elif self.book_if_borrowed(find_result[0]) == False:
                print("这本书未被借出！")
                return False
        else:
            print("数据库里没有这本书！")
            return False

    def book_continue_borrow(self, BookList, book_id, days):
        now=datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')
        find_result = self.book_find(BookList, 'book_id', book_id)
        if find_result:
            if self.book_if_borrowed(find_result[0]) == False:
                print("该书籍未被借阅！")
                return False
            elif self.book_if_borrowed(find_result[0]) == True:
                borrow_date_str = find_result[0].borrow_date # 记录下之前借的日期
                # borrow_date = datetime.datetime.strptime(borrow_date_str, '%Y-%m-%d %H:%M:%S')
                return_date_str = find_result[0].return_date # 记录下之前借的日期
                return_date = datetime.datetime.strptime(return_date_str, '%Y-%m-%d %H:%M:%S')
                delta = datetime.timedelta(days = days)
                now_return_date = return_date + delta
                now_return_date_str = now_return_date.strftime('%Y-%m-%d %H:%M:%S')
                find_result[0].return_date = now_return_date_str
                self.db_opt.borrow_state_change(book_id, borrow_date_str, return_date_str, if_continue_borrow=True)
                self.db_opt.record_add(now_str, '续借', self.reader_id, self.name, book_id, find_result[0].name, borrow_date_str, now_return_date_str, '正常')
                print("成功续借！")
                return True
        else:
            print("数据库里没有这本书！")
            return False



if __name__ == '__main__':
    rd = rd_opt('20120449')
    book_list = rd.BookList_init()
    reader_list = rd.ReaderList_init()
    record_list = rd.RecordList_init()
    #rd.book_borrow(book_list, "90376152", 2)
    #rd.book_continue_borrow(book_list,"90376152", 2)
    #rd.book_return(book_list, "90376152")
    #rd.books_info(book_list)
    #rd.readers_info(reader_list)
    #rd.records_info(record_list)
    find_result = rd.book_find(book_list, "name", "三国演义")
    #book_list = rd.book_shell_sort(book_list, 'borrow_times')
    rd.books_info(find_result)
    