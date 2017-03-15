# coding:utf8
import json

import time

import logging

import MySQLdb
from scrapy import FormRequest
from scrapy import Request
from scrapy.cmdline import execute
from scrapy.spiders import CrawlSpider

from ISpider.item.ModelItem import ModelItem
from ISpider.model.che168_ranke import RankInfo
from ISpider.resource.crawling_params import CRAWLING_CITIES, CRAWLING_SERIES, CRAWLING_PRICE
from ISpider.settings import *

__author__ = 'guangde'

mode = {
    'city'  : 1,
    'series': 2,
    'price' : 3,
}

PAGE_SIZE = 24

YEAR_CODE = 'ABCDEFGHJKLMNPRSTVWXY123456789'

class VINTest(CrawlSpider):
    name = 'vin_test'
    custom_settings = {
        'REDIRECT_ENABLED'      : False,
        'CONCURRENT_REQUESTS'   : 25,
        # 'DOWNLOAD_DELAY'   : 1,
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
        super(VINTest, self).__init__(*args, **kwargs)
        self.category = category
        self.vin_list = []
        if self.category:
            with open('%s/detail.csv' % RESOURCE_DIR, 'w+') as f:
                f.write('sub_VIN,VIN,Secret,厂家,品牌,车型,VIN年份,排放标准,进气形式,排量(升),最大马力(ps),驱动形式,变速器描述,档位数,燃油类型\n')
            with open('%s/vin-secret.txt' % RESOURCE_DIR, 'r+') as f:
                for line in f:
                    item = line.strip().split('\t')
                    vin_code = item[0]
                    secret = item[1]
                    self.vin_list.append((vin_code, secret))
        else:
            self.conn = MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD,
                                        db=MYSQL_DB, charset='utf8')
            cur = self.conn.cursor()
            cur.execute('select vin_code from vin_tmp where status=0')
            result = cur.fetchall()
            cur.close()
            self.conn.close()
            for res in result:
                self.vin_list.append(res[0])
            self.vin_list = list(set(self.vin_list))
            self.fp = None
        # self.logger = logging.getLogger()
    
    def start_requests(self):
        if self.category:
            for vin_code, secret in self.vin_list:
                yield Request('http://www.vin114.net/visitor/carmoduleinfo/index.jhtml?levelIds=%s&vinDate=%s' % (secret, get_year_by_vin(vin_code)),
                              meta={'type': 'getDetail', 'vin_code': vin_code, 'secret': secret},
                              dont_filter=True)
        else:
            for vin_code in self.vin_list:
                yield FormRequest('http://www.vin114.net/carpart/carmoduleinfo/vinresolve.jhtml',
                                  formdata={'vinCode': vin_code},
                                  meta={'type': 'getSecretCode', 'vin_code': vin_code},
                                  dont_filter=True)
    
    def parse(self, response):
        if response.meta['type'] == 'getSecretCode':
            try:
                data = json.loads(response.body_as_unicode())
            except Exception, e:
                self.logger.error(e)
            if data['code'] == 'S1':
                out_s = '%s,%s\n' % (response.meta['vin_code'], data['message']['levelIds'])
                self.logger.info(out_s.strip())
                self.fp = open('%s/out.txt' % RESOURCE_DIR, 'a+')
                self.fp.write(out_s)
                self.fp.close()
                # del self.vin_list[0]
                self.conn = MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD,
                                            db=MYSQL_DB, charset='utf8')
                cur = self.conn.cursor()
                cur.execute('update vin_tmp set status=1 where vin_code="%s"' % response.meta['vin_code'])
                self.conn.commit()
                cur.close()
                self.conn.close()
                yield None
            elif data['code'] == 'S0':
                self.logger.info('wrong code: %s' % response.meta['vin_code'])
                self.conn = MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD,
                                            db=MYSQL_DB, charset='utf8')
                cur = self.conn.cursor()
                cur.execute('update vin_tmp set status=-1 where vin_code="%s"' % response.meta['vin_code'])
                self.conn.commit()
                cur.close()
                self.conn.close()
                yield None
            elif data['code'] == 'E1':
                yield FormRequest('http://www.vin114.net/carpart/carmoduleinfo/vinresolve.jhtml',
                                  formdata={'vinCode': response.meta['vin_code']},
                                  meta={'type': 'getSecretCode', 'vin_code': response.meta['vin_code']},
                                  dont_filter=True)
        else:
            vin_code = response.meta['vin_code']
            secret = response.meta['secret']
            factory = response.xpath('//div[@class="mainhead"]/table/tr[1]/td[1]/text()').extract_first().strip()
            brand = response.xpath('//div[@class="mainhead"]/table/tr[1]/td[2]/text()').extract_first().strip()
            model = response.xpath('//div[@class="mainhead"]/table/tr[1]/td[3]/text()').extract_first().strip()
            vin_year = response.xpath('//div[@class="mainhead"]/table/tr[2]/td[1]/text()').extract_first().strip()
            emission = response.xpath('//div[@class="mainhead"]/table/tr[3]/td[2]/text()').extract_first().strip()
            ntake = response.xpath('//div[@class="mainhead"]/table/tr[1]/td[3]/text()').extract_first().strip()
            displacement = response.xpath('//div[@class="mainhead"]/table/tr[3]/td[1]/text()').extract_first().strip()
            max_horsepower = response.xpath('//div[@class="mainhead"]/table/tr[3]/td[2]/text()').extract_first().strip()
            driving_forms = response.xpath('//div[@class="mainhead"]/table/tr[3]/td[3]/text()').extract_first().strip()
            transmission = response.xpath('//div[@class="mainhead"]/table/tr[4]/td[1]/text()').extract_first().strip()
            gears = response.xpath('//div[@class="mainhead"]/table/tr[4]/td[2]/text()').extract_first().strip()
            fuel = response.xpath('//div[@class="mainhead"]/table/tr[4]/td[3]/text()').extract_first().strip()
            with open('%s/detail.csv' % RESOURCE_DIR, 'a+') as f:
                s = u'%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (
                    vin_code[:8] + vin_code[9:], vin_code, secret, factory, brand, model, vin_year, emission, ntake, displacement, max_horsepower, driving_forms, transmission, gears, fuel)
                f.write(s.encode('utf8'))
            print vin_code, secret
            yield None
    

def validate(vin_code):
    vin_code = vin_code.upper()
    if type(vin_code) == unicode:
        vin_code = vin_code.encode('utf8')
    # 位数校验
    if len(vin_code) != 17:
        return {'status': -1, 'msg': 'wrong vin code: wrong length'}
    # 字母合法性校验
    for i in vin_code:
        if i not in 'ABCDEFGHJKLMNPRSTUVWXYZ1234567890':
            return {'status': -1, 'msg': 'wrong vin code: illegal letter "%s"' % i}
    # 年份识别码校验
    # if get_year_code(model_name) != vin_code[9]:
    #     return False, 2
    # 地理区域识别码校验
    # if vin_code[0] not in GEOGRAPHICAL_REGION:
    #     return False, 'wrong geographical region code'
    # 过滤全数字 vin 码
    if vin_code.isdigit():
        return {'status': -1, 'msg': 'wrong vin code: all character are number'}
    # 过滤全字母 vin 码
    if vin_code.isalpha():
        return {'status': -1, 'msg': 'wrong vin code: all character are letter'}
    # 后三位均为数字
    if not vin_code[-3:].isdigit():
        return {'status': -1, 'msg': 'wrong vin code: last 3 characters are not all number'}
    return {'status': 0, 'msg': 'pass!'}

def get_year_by_vin(vin_code):
    temp = YEAR_CODE.find(vin_code[9])
    return 2010 + temp if 2010 + temp < 2017 else 2010 - (30 - temp)

if __name__ == '__main__':
    execute('scrapy crawl vin_test'.split(' '))
    # print get_year_by_vin('LEPM4ACC1D1A38907')
