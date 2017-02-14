# coding:utf8
import datetime

from peewee import *


from ISpider.util.DBManager import get_db

db = get_db()


class RankInfo(Model):
    id = CharField(100, primary_key=True)
    car_id = CharField(20, index=True)
    site = CharField(32)
    city = CharField(32)
    mode = IntegerField(11)
    ranking = TextField()
    date_create = DateTimeField(null=True, default=datetime.datetime.now())
    date_update = DateTimeField(null=True)

    class Meta:
        db_table = 'che168_rank'
        database = db


if __name__ == '__main__':
    test = RankInfo.create(car_id='test', ranking=22333)
