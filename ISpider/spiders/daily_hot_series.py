# coding:utf8
import json
import random

import time
import urllib2
from urllib import urlencode

from scrapy import Request
from scrapy.cmdline import execute
from scrapy.spiders import CrawlSpider

from ISpider.item.ModelItem import ModelItem
from ISpider.model.che168_daily_hot_series import HotSeries
from ISpider.resource.crawling_params import ALL_CITIES
from ISpider.util.Che168EncodingHelper import get_che168_udid, generate_che168_sign, encode_md5, encode_3des
from ISpider.util.ProxyUtil import get_random_proxy
from ISpider.util.StringUtil import StringUtil

__author__ = 'guangde'


class Che168DailyHotSeries(CrawlSpider):
    name = 'che168_daily_hot_series'
    
    custom_settings = {
        'REDIRECT_ENABLED'      : False,
        'CONCURRENT_REQUESTS'   : 10,
        'DOWNLOAD_TIMEOUT'      : 10,
        'RETRY_TIMES'           : 50,
        'DOWNLOADER_MIDDLEWARES': {
            'ISpider.middleware.middlewares.RemoveCookieMiddleware'     : 690,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
            'ISpider.middleware.middlewares.UserAgentMiddleware'        : 730,
            'ISpider.middleware.middlewares.RandomProxyMiddleware'      : 745,
        }
    }
    
    def __init__(self, category=None, *args, **kwargs):
        
        super(Che168DailyHotSeries, self).__init__(*args, **kwargs)
        self.category = category
        self.stringUtil = StringUtil()
    
    def start_requests(self):
        for city in ALL_CITIES:
            cid = city['CityId']
            pid = city['ProvinceId']
            data = {
                '_appid'    : '2scapp.ios',
                'appversion': '5.6.0',
                'channelid' : 'App Store',
                'cid'       : cid,
                'pid'       : pid,
                'udid'      : get_che168_udid()
            }
            sign = generate_che168_sign(data)
            # params = [(k, v) for k, v in data.items()]
            # params.sort(key=lambda d: d[0])
            # params.insert(1, ('_sign', sign))
            data['_sign'] = sign
            params_str = '&'.join(['%s=%s' % (k, v) for k, v in data.items()])
            # params_str = urlencode(data)
            # url = 'http://183.134.11.90/phone/v50/Cars/GetHotSeriesList.ashx?_appid=2scapp.ios&_sign=28d12efeb153d73b0062330adb2b10d1&appversion=5.6.0&channelid=App Store&cid=330200&pid=330000&udid=C/tHzFGCpFKy/pTflxfmHMua98hzCq3QfgZ+oaNoz/zWNGLEe0I0YE4lsxhcSzVJqoX7uZtDVRKYDWnj46Eg73dEh5vL6S0y'
            url = 'https://appsapi.che168.com/phone/v50/Cars/GetHotSeriesList.ashx?%s' % params_str
            # proxy_support = urllib2.ProxyHandler(
            #     {'http': 'http:%s' % get_random_proxy()})
            # opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
            # urllib2.install_opener(opener)
            # request = urllib2.Request(url)
            # request.add_header("User-Agent", 'UsedCar/5.6.0 (iPhone; iOS 10.2.1; Scale/2.00)')
            # request.add_header("Host", 'appsapi.che168.com')
            # content = urllib2.urlopen(request, timeout=5).read()
            # print content

            yield Request(url,
                          headers={'Host'      : 'appsapi.che168.com',
                                   'User-Agent': 'UsedCar/5.6.0 (iPhone; iOS 10.2.1; Scale/2.00)'},
                          meta={'city': city['CityName'], 'province': city['ProvinceName']}, dont_filter=True)
    
    def parse(self, response):
        data = json.loads(response.body_as_unicode())
        series_list = data['result']['list']
        for item in series_list:
            hs = HotSeries()
            hs.city = response.meta['city']
            hs.province = response.meta['province']
            hs.series = item['seriesname']
            hs.brand = item['brandname']
            hs.id = encode_md5('%s%s' % (hs.city.decode('utf8'), hs.series))
            mi = ModelItem()
            mi['model'] = [hs]
            yield mi


if __name__ == '__main__':
    execute('scrapy crawl che168_daily_hot_series'.split(' '))
