# coding:utf8
import json

import time

import logging
from scrapy import FormRequest
from scrapy import Request
from scrapy.cmdline import execute
from scrapy.spiders import CrawlSpider

from ISpider.item.ModelItem import ModelItem
from ISpider.model.che168_ranke import RankInfo
from ISpider.resource.crawling_params import CRAWLING_CITIES, CRAWLING_SERIES, CRAWLING_PRICE
from ISpider.settings import RESOURCE_DIR

__author__ = 'guangde'

mode = {
    'city'  : 1,
    'series': 2,
    'price' : 3,
}

PAGE_SIZE = 24

wrong_list = ['AFG465546ASDF4564',
'ASZXDXXED55254856',
'ASD4528963TH42188',
'BJJ8469HBDJ846694',
'CDXDK160106A68776',
'BVHJH976577668797',
'BDJSJWBUSBEU72837',
'BVGHH975688656787',
'BJK846VDJ84697496',
'CESFRCFFDCG356779',
'CFPM4ACC591E48231',
'CFPH4ABC491A83785',
'CFPM4ACC3F1A05197',
'FGHF4578356886546',
'F72H4ACC081A21661',
'CFPH5ABC469041821',
'FGTXZ1ADJ15438524',
'DGJGCRHH578YH6888',
'FLPM4ACC281A62493',
'GHBVFFCC785412369',
'GHJSJDBDJCHD73837',
'FLPM5ACP7P1A77384',
'GGHHHJYYHHHJJ4555',
'GMJ4952GWJ4956267',
'HFSRGVS5326090064',
'GJJHUHHGFFJJN8665',
'HDHHD645567664665',
'HDKN846BDJ8494843',
'GLMKD2G5CR5520196',
'JGFF8888888888888',
'HESC455HFC4480558',
'GJGHDUFFG55637698',
'GSUAF629461836827',
'JDK848JD846BD6496',
'HGLM5609871054389',
'GUJG56D5GGB556872',
'JKHDS1234656JK232',
'JJ144ACC7A1A15151',
'HDJ549NH846499496',
'JM5BL04R5A3332105',
'JGYBK174629283666',
'JDHH3645649675546',
'GZSM2ZGN67G276495',
'JM7GG443551157696',
'KDK67766764566685',
'GHHBB565588899478',
'L1367293947391046',
'L1234567891234567',
'L1FAB56DAF7654123',
'JM7GG443551157696',
'KFPM4ACC8C1E06213',
'JSHHDJ31254675546',
'KSUEBFA8641444700',
'LAWGM7952PWJ49562',
'LBD3GD2ET5D136654',
'JM6BL04Z1B2245115',
'LADC2NGT578497846',
'LBBDB11B2BD410964',
'LBED4925GW4926894',
'LBVDB11B8AD287881',
'LBEHDAE1309Y23569',
'LDF450646E5598462',
'LBDE9542WA9542685',
'L234JSW23JWZY0012',
'LDB634MAGD3G12336',
'L4784488447856787',
'LBEF9452GW9464264',
'LBDDHNVXGJ6758958',
'LBEMCZG86JM257852',
'LDFGHHHVVVCFFF458',
'LDGHBBBBBBB425668',
'LDGHGVVDFFGGH5326',
'LDAA6678287788876',
'LDHF5439184316816',
'LEFCVHJJJZGGGG123',
'LEPH4ABC071A23641',
'LEH513BRJ81873131',
'LEPH4ABC381A84098',
'LEP84ACC5E1A40436',
'LE425789654287639',
'LBH5846VV3J881669',
'LE5W3ANE7BB057816',
'LEPAA4ACC4B1E4675',
'LEPH4ABC491A00713',
'LEPH4ABC481E08093',
'LEPH4ABC391E19930',
'LEPH4ABCX91A24434',
'LEPH4ABC059035077',
'LEBAG6A3CD65D4687',
'LEPH4ABC291A30275',
'LEPH4ACC6A1E85357',
'LEPH4ACC9B1A35123',
'LEPH5ABC139023210',
'LEPH4ACC1A1A11722',
'LEPH4ABC691A38458',
'LEPH5ABC349015479',
'LDSAF321456789063',
'LEPH5ABC349010217',
'LEPH4ACCX91E19275',
'LEPH4ABC871A50401',
'LEPH4ACC591A52687',
'LEPH5ABC639024255',
'LEPH5ABC769042946',
'LEPH5ABC939027828',
'LEPH5ABC359039508',
'LEPH5ABC639023994',
'LEPM4ACC0A1E34824',
'LEPM4ACC0C1A84999',
'LEPM4ACC0C1E11403',
'LEPM4ACC0F1A48234',
'LEPM4ACC0A1F09392',
'LEPH4ABC381A88037',
'LEPH5ABC249006904',
'LEPM4ACC1E1A40822',
'LEPM4ACC1C1E00071',
'LEPM4ACC191E59761',
'LEPH4ABC581A82028',
'LEPM4ACC1C1A26903',
'LEPM4ACC1D1A38907',
'LEPM4ACC2A1E38650',
'LEPM4ACC291A40351',
'LEPH5ABC379017074',
'LEPM4ACC2B1A53588',
'LEPM4ACC3A1A61844',
'LEPH5ABC579019408',
'LEPM4ACC4A1E18612',
'LEPM4ACC4B1A15943',
'LEPM4ACC4B1E46654',
'LEPM4ACC481A22836',
'LEPM4ACC4C1A73899',
'LEPM4ACC1D1A50054',
'LEPM4ACC4A1E48645',
'LEPM4ACC4F1A88140',
'LEPM4ACC591F70827',
'LEPM4ACC4A1E91463',
'LEPM4ACC291A46540',
'LEPM4ACC2A1E38650',
'LEPM4ACC2B1A09039',
'LEPM4ACC4E1E05106',
'LEPM4ACC4D1A18568',
'LEPM4ACC5A1E88250',
'LEPM4ACC5C1A61573',
'LEPM4ACC5E1A20637',
'LEPM4ACC5F1A42736',
'LEPM4ACC5A1A47055',
'LEPM4ACC5D1A34861',
'LEPM4ACC691E72652',
'LEPM4ACC5C1A85422',
'LEPM4ACC5C1A85579',
'LEPM4ACC791E15795',
'LEPM4ACC6C1A75269',
'LEPM4ACC791E39952',
'LEPM4ACC8A1F36341',
'LEPM4ACC8B1A34687',
'LEPM4ACC791A92977',
'LEPM4ACC6D1A51846',
'LEPM4ACC8B1A60058',
'LEPM4ACC8B1A76597',
'LEPM4ACC3E1A04274',
'LEPM4ACC4E1A85592',
'LEPM4ACC7A1E98083',
'LEPM4ACC5F1A01619',
'LEPM4ACC8C1A85480',
'LEPM4ACC8D1A17648',
'LEPM4ACC7D1A15664',
'LEPM4ACC7D1A53573',
'LEPM4ACC9A1E90289',
'LEPM4ACC9D1A63408',
'LEPM4ACC9F1A74444',
'LEPM4ACCCA1F12034',
'LEPM4ACC8B1E34149',
'LEPM4ACC8C1A90338',
'LEPM4ACCXA1F08489',
'LEPM4ACC9A1A38472',
'LEPM4ACCXB1E48179',
'LEPM4ACCXA1E06819',
'LEPM4ACCXD1E12365',
'LEPM4ACCX91A69886',
'LEPM4ACP2A1A53169',
'LEPM4ACC8B1E41280',
'LEPM4ACC8E1A94134',
'LEPM4ACP4B1A47553',
'LEPM4ACCXD1A89404',
'LEPM4ACP1A1A08532',
'LEPM4ACP6B1E34847',
'LEPM4ACC9D1E19887',
'LEPM4ACP2E1A13650',
'LEPM4ACP7D1A36825',
'LEPM4ACP3D1A18547',
'LEPM4ACP7B1A73077',
'LEPM4ACC9B1A90928',
'LEPM4ACP9A1A34909',
'LEPM4ACP9B1A14113',
'LEPM4ACP8B1E30430',
'LEPM4ACP791E68788',
'LEPM4ACP8B1A73072',
'LEPM4ACPXA1F35646',
'LEPM4ADP381A16141',
'LEPM4AD80A1F11614',
'LEPM4ADP0D1A82771',
'LEPM4ACP4D1A11526',
]


class VINTest(CrawlSpider):
    name = 'vin_test'
    custom_settings = {
        'REDIRECT_ENABLED'      : False,
        'CONCURRENT_REQUESTS'   : 5,
        'DOWNLOAD_DELAY'   : 1,
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
        self.status = {}
        with open('%s/pass.grep' % RESOURCE_DIR, 'r+') as f:
            for line in f:
                vin_code = line.split('\t')[0]
                if validate(vin_code)['status'] == 0 and vin_code not in wrong_list:
                    self.vin_list.append(vin_code)
                    self.status[vin_code] = 0
        self.fp = None
        self.mode = mode[self.category or 'city']
        # self.logger = logging.getLogger()
    
    def start_requests(self):
        for vin_code in self.vin_list:
            yield FormRequest('http://www.vin114.net/carpart/carmoduleinfo/vinresolve.jhtml',
                              formdata={'vinCode': vin_code},
                              meta={'type': 'getSecretCode', 'vin_code': vin_code},
                              dont_filter=True)
    
    def parse(self, response):
        try:
            data = json.loads(response.body_as_unicode())
        except Exception, e:
            self.logger.error(e)
        if data['code'] == 'S1':
            out_s = '%s\t%s\n' % (response.meta['vin_code'], data['message']['levelIds'])
            self.logger.info(out_s.strip())
            self.fp = open('%s/out.txt' % RESOURCE_DIR, 'a+')
            self.fp.write(out_s)
            self.fp.close()
            # del self.vin_list[0]
            yield None
        elif data['code'] == 'S0':
            self.logger.info('wrong code: %s' % response.meta['vin_code'])
            # del self.vin_list[0]
            yield None
        elif data['code'] == 'E1':
            yield FormRequest('http://www.vin114.net/carpart/carmoduleinfo/vinresolve.jhtml',
                              formdata={'vinCode': response.meta['vin_code']},
                              meta={'type': 'getSecretCode', 'vin_code': response.meta['vin_code']},
                              dont_filter=True)
    

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
    

if __name__ == '__main__':
    execute('scrapy crawl vin_test'.split(' '))
