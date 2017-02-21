# coding:utf8
import json

import time

import datetime
from scrapy import Request
from scrapy.cmdline import execute
from scrapy.spiders import CrawlSpider

from ISpider.item.ModelItem import ModelItem
from ISpider.model.list_info import ListInfo
from ISpider.resource.crawling_params import CRAWLING_CITIES, CRAWLING_SERIES, CRAWLING_PRICE
from ISpider.util.StringUtil import StringUtil

__author__ = 'guangde'


mode = {
    'city': 1,
    'series': 2,
    'price': 3,
}

PAGE_SIZE = 24

class Che168ListInfo(CrawlSpider):
    name = 'che168_list_info'

    def __init__(self, category=None, *args, **kwargs):
        """

        :param category:
            值为 'series', 'price' 或不传，分别代表按 "城市和车系" 检索的排名、按 "城市和价格" 检索的排名、按 "城市" 检索的排名
        :param args:
        :param kwargs:
        """
        super(Che168ListInfo, self).__init__(*args, **kwargs)
        self.category = category
        self.stringUtil = StringUtil()

    def start_requests(self):
        for city in CRAWLING_CITIES:
            for series in CRAWLING_SERIES:
                url_prefix = 'https://appsapi.che168.com/Phone/V57/cars/search.ashx?_appid=2scapp.ios&appversion=5.5.9&channelid=App Store&cid=%s&cpcnum=4&dealertype=9&ispic=0&orderby=0&pagesize=%s&pid=%s&seriesid=%s&brandid=%s&_sign=cda602a1e47e463968fdbe03a58f04a3' % (city['city_id'], PAGE_SIZE, city['province_id'], series['series_id'], series['brand_id'])
                yield Request('%s&pageindex=1' % url_prefix, meta={'type': 'get_total', 'page': 1, 'mode': 2, 'city_name': city['name'], 'series': series}, dont_filter=True)
        for city in CRAWLING_CITIES:
            for price in CRAWLING_PRICE:
                url_prefix = 'https://appsapi.che168.com/Phone/V57/cars/search.ashx?_appid=2scapp.ios&appversion=5.5.9&channelid=App Store&cid=%s&cpcnum=4&dealertype=9&ispic=0&orderby=0&pagesize=%s&pid=%s&priceregion=%s&_sign=cda602a1e47e463968fdbe03a58f04a3' % (city['city_id'], PAGE_SIZE, city['province_id'], price)
                yield Request('%s&pageindex=1' % url_prefix, meta={'type': 'get_total', 'page': 1, 'mode': 3, 'city_name': city['name'], 'price': price}, dont_filter=True)
        for city in CRAWLING_CITIES:
            url_prefix = 'https://appsapi.che168.com/Phone/V57/cars/search.ashx?_appid=2scapp.ios&appversion=5.5.9&channelid=App Store&cid=%s&cpcnum=4&dealertype=9&ispic=0&orderby=0&pagesize=%s&pid=%s&_sign=cda602a1e47e463968fdbe03a58f04a3' % (city['city_id'], PAGE_SIZE, city['province_id'])
            yield Request('%s&pageindex=1' % url_prefix, meta={'type': 'get_total', 'page': 1, 'mode': 1, 'city_name': city['name']}, dont_filter=True)

    def parse(self, response):
        try:
            data = json.loads(response.body_as_unicode())
        except Exception, e:
            print e
        total = data['result']['rowcount']
        li = ListInfo()
        if response.meta.get('series'):
            li.series = response.meta.get('series')
        if li.series:
            li.series = li.series['series_name']
        li.city = response.meta.get('city_name')
        if response.meta.get('price'):
            li.price = response.meta.get('price')
        li.id = self.stringUtil.md5_encode('%s_%s_%s' % (li.city, (li.series or li.price or 'None'), datetime.datetime.now().strftime('%Y-%m-%d %H:00:00')))
        li.query_mode = response.meta['mode']
        li.total_count = total
        li.page_count = data['result']['pagecount']

        mi = ModelItem()
        mi['model'] = [li]
        yield mi


if __name__ == '__main__':
    execute('scrapy crawl che168_list_info'.split(' '))
