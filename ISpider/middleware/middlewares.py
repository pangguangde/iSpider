# coding:utf8
from ISpider.util.ProxyUtil import *

__author__ = 'pangguangde'


class UserAgentMiddleware(object):

    def process_request(self, request, spider):
        ua = get_random_ua()
        if ua:
            request.headers['User-Agent'] = ua

    def process_exception(self, request, exception, spider):
        ua = get_random_ua()
        request.headers['User-Agent'] = ua

class RemoveCookieMiddleware(object):
    def process_request(self, request, spider):
        request.cookies = {}
        if 'Cookie' in request.headers:
            request.headers['Cookie'] = ''
        request.headers['cookies'] = ''

    def process_exception(self, request, exception, spider):
        request.cookies = {}
        request.headers['cookies'] = ''
        if 'Cookie' in request.headers:
            request.headers['Cookie'] = ''

class RandomProxyMiddleware(object):
    def process_request(self, request, spider):
        res = get_random_proxy()
        request.meta['proxy'] = 'http://%s' % res

    def process_exception(self, request, exception, spider):
        res = get_random_proxy()
        request.meta['proxy'] = 'http://%s' % res
        if str(exception).find('Connection was refused by other side: 61: Connection refused.') > -1:
            if 'Cookie' in request.headers:
                request.headers.pop('Cookie')
            return request
