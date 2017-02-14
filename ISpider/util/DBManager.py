# coding:utf8
from peewee import MySQLDatabase

from ISpider.settings import *

__author__ = 'pangguangde'

db = MySQLDatabase(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, database=MYSQL_DB, charset='utf8', port=MYSQL_PORT)


def get_db():
    return db
