# coding:utf8
import json

import time
from scrapy import Request
from scrapy.cmdline import execute
from scrapy.spiders import CrawlSpider

from ISpider.item.ModelItem import ModelItem
from ISpider.model.che168_ranke import RankInfo
from ISpider.resource.crawling_params import CRAWLING_CITIES, CRAWLING_SERIES, CRAWLING_PRICE

__author__ = 'guangde'

mode = {
    'city'  : 1,
    'series': 2,
    'price' : 3,
}

PAGE_SIZE = 24


class Che168Rank(CrawlSpider):
    name = 'che168_rank'
    custom_settings = {
        'REDIRECT_ENABLED'      : False,
        'CONCURRENT_REQUESTS'   : 10,
        'DOWNLOAD_TIMEOUT'      : 10,
        'RETRY_TIMES'           : 50,
        'ITEM_PIPELINES'        : {
            'ISpider.pipelines.ISpiderRankInfoPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'ISpider.middleware.middlewares.RemoveCookieMiddleware'     : 690,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
            'ISpider.middleware.middlewares.UserAgentMiddleware'        : 730,
            'ISpider.middleware.middlewares.RandomProxyMiddleware'      : 745,
        }
    }
    
    def __init__(self, category=None, *args, **kwargs):
        """

        :param category:
            值为 'series', 'price' 或不传，分别代表按 "城市和车系" 检索的排名、按 "城市和价格" 检索的排名、按 "城市" 检索的排名
        :param args:
        :param kwargs:
        """
        super(Che168Rank, self).__init__(*args, **kwargs)
        self.category = category
        self.mode = mode[self.category or 'city']
    
    def start_requests(self):
        for page in range(1, 6):
            if self.category == 'series':
                for city in CRAWLING_CITIES:
                    for series in CRAWLING_SERIES:
                        url_prefix = 'https://appsapi.che168.com/Phone/V57/cars/search.ashx?_appid=2scapp.ios&appversion=5.5.9&channelid=App Store&cid=%s&cpcnum=4&dealertype=9&ispic=0&orderby=0&pagesize=%s&pid=%s&seriesid=%s&brandid=%s&_sign=cda602a1e47e463968fdbe03a58f04a3' % (
                        city['city_id'], PAGE_SIZE, city['province_id'], series['series_id'], series['brand_id'])
                        yield Request('%s&pageindex=%s' % (url_prefix, page),
                                      meta={'url_prefix': url_prefix, 'type': 'get_cars_info', 'page': page,
                                            'city_name' : city['name']}, dont_filter=True)
            elif self.category == 'price':
                for city in CRAWLING_CITIES:
                    for price in CRAWLING_PRICE:
                        url_prefix = 'https://appsapi.che168.com/Phone/V57/cars/search.ashx?_appid=2scapp.ios&appversion=5.5.9&channelid=App Store&cid=%s&cpcnum=4&dealertype=9&ispic=0&orderby=0&pagesize=%s&pid=%s&priceregion=%s&_sign=cda602a1e47e463968fdbe03a58f04a3' % (
                        city['city_id'], PAGE_SIZE, city['province_id'], price)
                        yield Request('%s&pageindex=%s' % (url_prefix, page),
                                      meta={'url_prefix': url_prefix, 'type': 'get_cars_info', 'page': page,
                                            'city_name' : city['name']}, dont_filter=True)
            else:
                for city in CRAWLING_CITIES:
                    url_prefix = 'https://appsapi.che168.com/Phone/V57/cars/search.ashx?_appid=2scapp.ios&appversion=5.5.9&channelid=App Store&cid=%s&cpcnum=4&dealertype=9&ispic=0&orderby=0&pagesize=%s&pid=%s&_sign=cda602a1e47e463968fdbe03a58f04a3' % (
                    city['city_id'], PAGE_SIZE, city['province_id'])
                    yield Request('%s&pageindex=%s' % (url_prefix, page),
                                  meta={'url_prefix': url_prefix, 'type': 'get_cars_info', 'page': page,
                                        'city_name' : city['name']}, dont_filter=True)
    
    def parse(self, response):
        if response.meta['type'] == 'get_total':
            pass
            # try:
            #     data = json.loads(response.body_as_unicode())
            # except Exception, e:
            #     print e
            # total = data['result']['rowcount']
            # pages = (total / 10  + 1) / PAGE_SIZE + 1
            # if pages > 1:
            #     for page in range(1, pages + 1):
            #         yield Request('%s&pageindex=%s' % (response.meta['url_prefix'], page), meta={'type': 'get_cars_info', 'page': page, 'city_name': response.meta['city_name']}, dont_filter=True)
            # else:
            #     self.parse_cars_info(response)
        else:
            for item in self.parse_cars_info(response):
                yield item
    
    def parse_cars_info(self, response):
        try:
            data = json.loads(response.body_as_unicode())
        except Exception, e:
            print e
        car_list = data['result']['carlist']
        page_size = len(car_list)
        if page_size:
            for i in range(page_size):
                car_info = car_list[i]
                ri = RankInfo()
                ri.site = 'che168'
                ri.city = response.meta['city_name']
                ri.mode = self.mode
                ri.car_id = str(car_info['carid'])
                ri.id = '%s_%s_%s' % (ri.site, ri.car_id, ri.mode)
                ri.ranking = json.dumps({int(time.time()): i + 1 + (response.meta[
                                                                        'page'] - 1) * PAGE_SIZE})  # cause ranking start from 1 while list indices start from 0
                mi = ModelItem()
                mi['model'] = [ri]
                yield mi


if __name__ == '__main__':
    execute('scrapy crawl che168_rank -a category=series'.split(' '))
