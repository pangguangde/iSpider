# coding:utf8
import datetime

from peewee import *


from ISpider.util.DBManager import get_db

db = get_db()


class HotSeries(Model):
    id = CharField(100, primary_key=True)
    city = CharField(32, index=True, null=False)
    province = CharField(32, index=True, null=True)
    brand = CharField(100, index=True, null=False)
    series = CharField(200, index=True, null=False)
    date_create = DateTimeField(null=True, default=datetime.datetime.now())
    date_update = DateTimeField(null=True)

    class Meta:
        db_table = 'daily_hot_series'
        database = db


if __name__ == '__main__':
    HotSeries.create_table()
