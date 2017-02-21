# coding:utf8
import datetime

from peewee import *


from ISpider.util.DBManager import get_db

db = get_db()


class ListInfo(Model):
    id = CharField(primary_key=True)
    
    series = CharField(200, index=True, null=True)
    city = CharField(32, index=True, null=True)
    price = CharField(32, index=True, null=True)
    
    query_mode = IntegerField(11)
    total_count = IntegerField(11)
    page_count = IntegerField(11)
    date_create = DateTimeField(null=True, default=datetime.datetime.now())
    date_update = DateTimeField(null=True)

    class Meta:
        db_table = 'list_info'
        database = db


if __name__ == '__main__':
    ListInfo.create_table()
