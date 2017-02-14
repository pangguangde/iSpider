# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime

from ISpider.util.DBManager import get_db

class ISpiderPipeline():
    def __init__(self):
        self.db = get_db()

    def process_item(self, item, spider):
        for obj in item['model']:
            with self.db.atomic():
                try:
                    model = type(obj)()
                    model.get(id=obj.id)
                    obj.save()
                    spider.logger.info('pipeline : mysql %s : {id: %s}' % ('update', obj.id))
                except:
                    obj.save(force_insert=True)
                    spider.logger.info('pipeline : mysql %s : {id: %s}' % ('insert', obj.id))
        return item

    def close_spider(self, spider):
        print spider.crawler.stats._stats


if __name__ == '__main__':
    pass
