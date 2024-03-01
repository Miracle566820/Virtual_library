
# Create your models here.
from django.db import models
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



