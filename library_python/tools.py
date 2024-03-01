from re import I
import time
import string
import random

def date_compare(date1, date2):   # 比较时间函数
    try:
        time1 = time.mktime(time.strptime(date1, '%Y-%m-%d'))
        time2 = time.mktime(time.strptime(date2, '%Y-%m-%d'))
        #日期转化为int比较
        diff = int(time1)-int(time2)
        # print(diff)
        if diff > 0:
            return 1
        elif diff == 0:
            return 0
        else:
            return -1
    except Exception as e:
        print(e)
        return ''

def generate_book_id(): # 随机生成book_id，不会有重复
    seeds = string.digits
    random_str = random.sample(seeds, k=4)
    return ("".join(random_str))

def generate_operate_id(): # 随机生成operate_id，不会有重复，每个id对应一个归还、借阅、续借操作
    seeds = string.digits
    random_str = random.sample(seeds, k=4)
    return ("".join(random_str))
