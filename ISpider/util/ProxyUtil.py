# coding:utf8
import random
import re

import requests

from ISpider.settings import PROXYPOOL_URL
from ISpider.util.ResUtil import ResUtil

__author__ = 'pangguangde'

PROXY_RE = re.compile('\d+\.\d+\.\d+\.\d+')
ua_list = ResUtil().json_loader('user_agent.json')

def get_from_url(url):
	retryTime = 20
	res = None
	for i in range(retryTime):
		try:
			res = requests.get(url)  # self.proxyUtil.getRandomProxy())
			if res.status_code != 200:
				continue
			break
		except:
			continue
	return res

def get_random_ua():
	return random.choice(ua_list)

def get_random_proxy():
	res = get_from_url(PROXYPOOL_URL)
	return res.text

if __name__ == '__main__':
	import time
	for i in range(10):
		print get_random_proxy()
		time.sleep(1)

