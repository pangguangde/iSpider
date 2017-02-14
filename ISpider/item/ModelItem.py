# coding:utf8
import scrapy

__author__ = 'pangguangde'


class ModelItem(scrapy.Item):
    model = scrapy.Field()

    @classmethod
    def getInstance(cls, model):
        modelItem = cls()
        modelItem['model'] = model
        return modelItem