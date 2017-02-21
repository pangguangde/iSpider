# coding:utf8
import json

import time
from scrapy import Request
from scrapy.cmdline import execute
from scrapy.spiders import CrawlSpider

from ISpider.item.ModelItem import ModelItem
from ISpider.model.che168_ranke import RankInfo

__author__ = 'guangde'


mode = {
    'city': 1,
    'series': 2,
    'price': 3,
}

crawling_price = [
    '0-3',
    '3-5',
    '5-10',
    '10-15',
    '15-20',
    '20-30',
    '30-50',
    '50-65535',
]

crawling_cities = [
    {
        'name'   : u'宁波',
        'province_id': '330000',
        'city_id': 330200
    }, {
        'name'   : u'佛山',
        'province_id': '440000',
        'city_id': 440600
    }, {
        'name'   : u'太原',
        'province_id': '140000',
        'city_id': 140100
    }, {
        'name'   : u'杭州',
        'province_id': '330000',
        'city_id': 330100
    }
]

crawling_series = [
    {"factoryid": u"58", "series_name": u"POLO", "brand_name": u"大众", "factory": u"上汽大众", "series_id": u"145", "brand_id": u"1"},
    {"factoryid": u"58", "series_name": u"桑塔纳", "brand_name": u"大众", "factory": u"上汽大众", "series_id": u"2922", "brand_id": u"1"},
    {"factoryid": u"58", "series_name": u"朗行", "brand_name": u"大众", "factory": u"上汽大众", "series_id": u"3103", "brand_id": u"1"},
    {"factoryid": u"58", "series_name": u"朗逸", "brand_name": u"大众", "factory": u"上汽大众", "series_id": u"614", "brand_id": u"1"},
    {"factoryid": u"58", "series_name": u"朗境", "brand_name": u"大众", "factory": u"上汽大众", "series_id": u"3197", "brand_id": u"1"},
    {"factoryid": u"58", "series_name": u"凌渡", "brand_name": u"大众", "factory": u"上汽大众", "series_id": u"3457", "brand_id": u"1"},
    {"factoryid": u"58", "series_name": u"帕萨特", "brand_name": u"大众", "factory": u"上汽大众", "series_id": u"528", "brand_id": u"1"},
    {"factoryid": u"58", "series_name": u"途观", "brand_name": u"大众", "factory": u"上汽大众", "series_id": u"874", "brand_id": u"1"},
    {"factoryid": u"58", "series_name": u"途安", "brand_name": u"大众", "factory": u"上汽大众", "series_id": u"333", "brand_id": u"1"},
    {"factoryid": u"58", "series_name": u"高尔", "brand_name": u"大众", "factory": u"上汽大众", "series_id": u"144", "brand_id": u"1"},
    {"factoryid": u"58", "series_name": u"Passat领驭", "brand_name": u"大众", "factory": u"上汽大众", "series_id": u"826", "brand_id": u"1"},
    {"factoryid": u"58", "series_name": u"桑塔纳经典", "brand_name": u"大众", "factory": u"上汽大众", "series_id": u"149", "brand_id": u"1"},
    {"factoryid": u"58", "series_name": u"桑塔纳志俊", "brand_name": u"大众", "factory": u"上汽大众", "series_id": u"207", "brand_id": u"1"},
    {"factoryid": u"8", "series_name": u"捷达", "brand_name": u"大众", "factory": u"一汽-大众", "series_id": u"16", "brand_id": u"1"},
    {"factoryid": u"8", "series_name": u"宝来", "brand_name": u"大众", "factory": u"一汽-大众", "series_id": u"633", "brand_id": u"1"},
    {"factoryid": u"8", "series_name": u"高尔夫", "brand_name": u"大众", "factory": u"一汽-大众", "series_id": u"871", "brand_id": u"1"},
    {"factoryid": u"8", "series_name": u"速腾", "brand_name": u"大众", "factory": u"一汽-大众", "series_id": u"442", "brand_id": u"1"},
    {"factoryid": u"8", "series_name": u"高尔夫・嘉旅", "brand_name": u"大众", "factory": u"一汽-大众", "series_id": u"3964", "brand_id": u"1"},
    {"factoryid": u"8", "series_name": u"迈腾", "brand_name": u"大众", "factory": u"一汽-大众", "series_id": u"496", "brand_id": u"1"},
    {"factoryid": u"8", "series_name": u"一汽-大众CC", "brand_name": u"大众", "factory": u"一汽-大众", "series_id": u"905", "brand_id": u"1"},
    {"factoryid": u"8", "series_name": u"宝来/宝来经典", "brand_name": u"大众", "factory": u"一汽-大众", "series_id": u"15", "brand_id": u"1"},
    {"factoryid": u"8", "series_name": u"开迪", "brand_name": u"大众", "factory": u"一汽-大众", "series_id": u"360", "brand_id": u"1"},
    {"factoryid": u"50", "series_name": u"大众up!", "brand_name": u"大众", "factory": u"大众(进口)", "series_id": u"780", "brand_id": u"1"},
    {"factoryid": u"50", "series_name": u"甲壳虫", "brand_name": u"大众", "factory": u"大众(进口)", "series_id": u"210", "brand_id": u"1"},
    {"factoryid": u"50", "series_name": u"高尔夫(进口)", "brand_name": u"大众", "factory": u"大众(进口)", "series_id": u"372", "brand_id": u"1"},
    {"factoryid": u"50", "series_name": u"蔚揽", "brand_name": u"大众", "factory": u"大众(进口)", "series_id": u"3999", "brand_id": u"1"},
    {"factoryid": u"50", "series_name": u"辉腾", "brand_name": u"大众", "factory": u"大众(进口)", "series_id": u"224", "brand_id": u"1"},
    {"factoryid": u"50", "series_name": u"Tiguan", "brand_name": u"大众", "factory": u"大众(进口)", "series_id": u"557", "brand_id": u"1"},
    {"factoryid": u"50", "series_name": u"途锐", "brand_name": u"大众", "factory": u"大众(进口)", "series_id": u"82", "brand_id": u"1"},
    {"factoryid": u"50", "series_name": u"夏朗", "brand_name": u"大众", "factory": u"大众(进口)", "series_id": u"86", "brand_id": u"1"},
    {"factoryid": u"50", "series_name": u"迈特威", "brand_name": u"大众", "factory": u"大众(进口)", "series_id": u"631", "brand_id": u"1"},
    {"factoryid": u"50", "series_name": u"凯路威", "brand_name": u"大众", "factory": u"大众(进口)", "series_id": u"3416", "brand_id": u"1"},
    {"factoryid": u"50", "series_name": u"尚酷", "brand_name": u"大众", "factory": u"大众(进口)", "series_id": u"669", "brand_id": u"1"},
    {"factoryid": u"50", "series_name": u"Passat", "brand_name": u"大众", "factory": u"大众(进口)", "series_id": u"368", "brand_id": u"1"},
    {"factoryid": u"50", "series_name": u"大众CC", "brand_name": u"大众", "factory": u"大众(进口)", "series_id": u"700", "brand_id": u"1"},
    {"factoryid": u"50", "series_name": u"大众Eos", "brand_name": u"大众", "factory": u"大众(进口)", "series_id": u"430", "brand_id": u"1"},
    {"factoryid": u"50", "series_name": u"迈腾(进口)", "brand_name": u"大众", "factory": u"大众(进口)", "series_id": u"539", "brand_id": u"1"},
    {"factoryid": u"155", "series_name": u"YARiS L 致炫", "brand_name": u"丰田", "factory": u"广汽丰田", "series_id": u"3126", "brand_id": u"3"},
    {"factoryid": u"155", "series_name": u"雷凌", "brand_name": u"丰田", "factory": u"广汽丰田", "series_id": u"3462", "brand_id": u"3"},
    {"factoryid": u"155", "series_name": u"凯美瑞", "brand_name": u"丰田", "factory": u"广汽丰田", "series_id": u"110", "brand_id": u"3"},
    {"factoryid": u"155", "series_name": u"汉兰达", "brand_name": u"丰田", "factory": u"广汽丰田", "series_id": u"771", "brand_id": u"3"},
    {"factoryid": u"155", "series_name": u"逸致", "brand_name": u"丰田", "factory": u"广汽丰田", "series_id": u"2237", "brand_id": u"3"},
    {"factoryid": u"155", "series_name": u"雅力士", "brand_name": u"丰田", "factory": u"广汽丰田", "series_id": u"505", "brand_id": u"3"},
    {"factoryid": u"40", "series_name": u"威驰", "brand_name": u"丰田", "factory": u"一汽丰田", "series_id": u"111", "brand_id": u"3"},
    {"factoryid": u"40", "series_name": u"花冠", "brand_name": u"丰田", "factory": u"一汽丰田", "series_id": u"109", "brand_id": u"3"},
    {"factoryid": u"40", "series_name": u"卡罗拉", "brand_name": u"丰田", "factory": u"一汽丰田", "series_id": u"526", "brand_id": u"3"},
    {"factoryid": u"40", "series_name": u"普锐斯", "brand_name": u"丰田", "factory": u"一汽丰田", "series_id": u"371", "brand_id": u"3"},
    {"factoryid": u"40", "series_name": u"锐志", "brand_name": u"丰田", "factory": u"一汽丰田", "series_id": u"375", "brand_id": u"3"},
    {"factoryid": u"40", "series_name": u"皇冠", "brand_name": u"丰田", "factory": u"一汽丰田", "series_id": u"882", "brand_id": u"3"},
    {"factoryid": u"40", "series_name": u"一汽丰田RAV4", "brand_name": u"丰田", "factory": u"一汽丰田", "series_id": u"770", "brand_id": u"3"},
    {"factoryid": u"40", "series_name": u"兰德酷路泽", "brand_name": u"丰田", "factory": u"一汽丰田", "series_id": u"45", "brand_id": u"3"},
    {"factoryid": u"40", "series_name": u"普拉多", "brand_name": u"丰田", "factory": u"一汽丰田", "series_id": u"46", "brand_id": u"3"},
    {"factoryid": u"40", "series_name": u"柯斯达", "brand_name": u"丰田", "factory": u"一汽丰田", "series_id": u"2527", "brand_id": u"3"},
    {"factoryid": u"40", "series_name": u"特锐", "brand_name": u"丰田", "factory": u"一汽丰田", "series_id": u"170", "brand_id": u"3"},
    {"factoryid": u"63", "series_name": u"FJ 酷路泽", "brand_name": u"丰田", "factory": u"丰田(进口)", "series_id": u"513", "brand_id": u"3"},
    {"factoryid": u"63", "series_name": u"Fortuner", "brand_name": u"丰田", "factory": u"丰田(进口)", "series_id": u"3851", "brand_id": u"3"},
    {"factoryid": u"63", "series_name": u"威飒", "brand_name": u"丰田", "factory": u"丰田(进口)", "series_id": u"762", "brand_id": u"3"},
    {"factoryid": u"63", "series_name": u"红杉", "brand_name": u"丰田", "factory": u"丰田(进口)", "series_id": u"964", "brand_id": u"3"},
    {"factoryid": u"63", "series_name": u"埃尔法", "brand_name": u"丰田", "factory": u"丰田(进口)", "series_id": u"2107", "brand_id": u"3"},
    {"factoryid": u"63", "series_name": u"普瑞维亚", "brand_name": u"丰田", "factory": u"丰田(进口)", "series_id": u"107", "brand_id": u"3"},
    {"factoryid": u"63", "series_name": u"Sienna", "brand_name": u"丰田", "factory": u"丰田(进口)", "series_id": u"983", "brand_id": u"3"},
    {"factoryid": u"63", "series_name": u"丰田86", "brand_name": u"丰田", "factory": u"丰田(进口)", "series_id": u"2574", "brand_id": u"3"},
    {"factoryid": u"63", "series_name": u"杰路驰", "brand_name": u"丰田", "factory": u"丰田(进口)", "series_id": u"2244", "brand_id": u"3"},
    {"factoryid": u"63", "series_name": u"HIACE", "brand_name": u"丰田", "factory": u"丰田(进口)", "series_id": u"2607", "brand_id": u"3"},
    {"factoryid": u"63", "series_name": u"坦途", "brand_name": u"丰田", "factory": u"丰田(进口)", "series_id": u"2354", "brand_id": u"3"},
    {"factoryid": u"63", "series_name": u"凯美瑞(海外)", "brand_name": u"丰田", "factory": u"丰田(进口)", "series_id": u"963", "brand_id": u"3"},
    {"factoryid": u"63", "series_name": u"丰田RAV4(进口)", "brand_name": u"丰田", "factory": u"丰田(进口)", "series_id": u"206", "brand_id": u"3"},
    {"factoryid": u"63", "series_name": u"汉兰达(进口)", "brand_name": u"丰田", "factory": u"丰田(进口)", "series_id": u"549", "brand_id": u"3"},
    {"factoryid": u"63", "series_name": u"兰德酷路泽(进口)", "brand_name": u"丰田", "factory": u"丰田(进口)", "series_id": u"550", "brand_id": u"3"},
    {"factoryid": u"63", "series_name": u"普拉多(进口)", "brand_name": u"丰田", "factory": u"丰田(进口)", "series_id": u"334", "brand_id": u"3"},
    {"factoryid": u"43", "series_name": u"嘉年华", "brand_name": u"福特", "factory": u"长安福特", "series_id": u"659", "brand_id": u"8"},
    {"factoryid": u"43", "series_name": u"福克斯", "brand_name": u"福特", "factory": u"长安福特", "series_id": u"364", "brand_id": u"8"},
    {"factoryid": u"43", "series_name": u"福睿斯", "brand_name": u"福特", "factory": u"长安福特", "series_id": u"3347", "brand_id": u"8"},
    {"factoryid": u"43", "series_name": u"蒙迪欧", "brand_name": u"福特", "factory": u"长安福特", "series_id": u"117", "brand_id": u"8"},
    {"factoryid": u"43", "series_name": u"致胜", "brand_name": u"福特", "factory": u"长安福特", "series_id": u"3175", "brand_id": u"8"},
    {"factoryid": u"43", "series_name": u"金牛座", "brand_name": u"福特", "factory": u"长安福特", "series_id": u"3693", "brand_id": u"8"},
    {"factoryid": u"43", "series_name": u"翼搏", "brand_name": u"福特", "factory": u"长安福特", "series_id": u"2871", "brand_id": u"8"},
    {"factoryid": u"43", "series_name": u"翼虎", "brand_name": u"福特", "factory": u"长安福特", "series_id": u"2863", "brand_id": u"8"},
    {"factoryid": u"43", "series_name": u"锐界", "brand_name": u"福特", "factory": u"长安福特", "series_id": u"3615", "brand_id": u"8"},
    {"factoryid": u"43", "series_name": u"麦柯斯", "brand_name": u"福特", "factory": u"长安福特", "series_id": u"498", "brand_id": u"8"},
    {"factoryid": u"43", "series_name": u"蒙迪欧-致胜", "brand_name": u"福特", "factory": u"长安福特", "series_id": u"577", "brand_id": u"8"},
    {"factoryid": u"447", "series_name": u"撼路者", "brand_name": u"福特", "factory": u"江铃福特", "series_id": u"3518", "brand_id": u"8"},
    {"factoryid": u"447", "series_name": u"途睿欧", "brand_name": u"福特", "factory": u"江铃福特", "series_id": u"3814", "brand_id": u"8"},
    {"factoryid": u"447", "series_name": u"经典全顺", "brand_name": u"福特", "factory": u"江铃福特", "series_id": u"2523", "brand_id": u"8"},
    {"factoryid": u"447", "series_name": u"新世代全顺", "brand_name": u"福特", "factory": u"江铃福特", "series_id": u"2524", "brand_id": u"8"},
    {"factoryid": u"61", "series_name": u"福特GT", "brand_name": u"福特", "factory": u"福特(进口)", "series_id": u"378", "brand_id": u"8"},
    {"factoryid": u"61", "series_name": u"嘉年华(进口)", "brand_name": u"福特", "factory": u"福特(进口)", "series_id": u"713", "brand_id": u"8"},
    {"factoryid": u"61", "series_name": u"福克斯(进口)", "brand_name": u"福特", "factory": u"福特(进口)", "series_id": u"704", "brand_id": u"8"},
    {"factoryid": u"61", "series_name": u"探险者", "brand_name": u"福特", "factory": u"福特(进口)", "series_id": u"2024", "brand_id": u"8"},
    {"factoryid": u"61", "series_name": u"福特E350", "brand_name": u"福特", "factory": u"福特(进口)", "series_id": u"2302", "brand_id": u"8"},
    {"factoryid": u"61", "series_name": u"Mustang", "brand_name": u"福特", "factory": u"福特(进口)", "series_id": u"102", "brand_id": u"8"},
    {"factoryid": u"61", "series_name": u"福特F-150", "brand_name": u"福特", "factory": u"福特(进口)", "series_id": u"2353", "brand_id": u"8"},
    {"factoryid": u"61", "series_name": u"Kuga", "brand_name": u"福特", "factory": u"福特(进口)", "series_id": u"97", "brand_id": u"8"},
    {"factoryid": u"61", "series_name": u"锐界(进口)", "brand_name": u"福特", "factory": u"福特(进口)", "series_id": u"684", "brand_id": u"8"},
    {"factoryid": u"61", "series_name": u"征服者", "brand_name": u"福特", "factory": u"福特(进口)", "series_id": u"2025", "brand_id": u"8"},
    {"factoryid": u"9", "series_name": u"奥迪A3", "brand_name": u"奥迪", "factory": u"一汽-大众奥迪", "series_id": u"3170", "brand_id": u"33"},
    {"factoryid": u"9", "series_name": u"奥迪A4L", "brand_name": u"奥迪", "factory": u"一汽-大众奥迪", "series_id": u"692", "brand_id": u"33"},
    {"factoryid": u"9", "series_name": u"奥迪A6L", "brand_name": u"奥迪", "factory": u"一汽-大众奥迪", "series_id": u"18", "brand_id": u"33"},
    {"factoryid": u"9", "series_name": u"奥迪Q3", "brand_name": u"奥迪", "factory": u"一汽-大众奥迪", "series_id": u"2951", "brand_id": u"33"},
    {"factoryid": u"9", "series_name": u"奥迪Q5", "brand_name": u"奥迪", "factory": u"一汽-大众奥迪", "series_id": u"812", "brand_id": u"33"},
    {"factoryid": u"9", "series_name": u"奥迪A4", "brand_name": u"奥迪", "factory": u"一汽-大众奥迪", "series_id": u"19", "brand_id": u"33"},
    {"factoryid": u"9", "series_name": u"奥迪A6", "brand_name": u"奥迪", "factory": u"一汽-大众奥迪", "series_id": u"509", "brand_id": u"33"},
    {"factoryid": u"79", "series_name": u"奥迪A1", "brand_name": u"奥迪", "factory": u"奥迪(进口)", "series_id": u"650", "brand_id": u"33"},
    {"factoryid": u"79", "series_name": u"奥迪A3(进口)", "brand_name": u"奥迪", "factory": u"奥迪(进口)", "series_id": u"370", "brand_id": u"33"},
    {"factoryid": u"79", "series_name": u"奥迪S3", "brand_name": u"奥迪", "factory": u"奥迪(进口)", "series_id": u"2730", "brand_id": u"33"},
    {"factoryid": u"79", "series_name": u"奥迪A4(进口)", "brand_name": u"奥迪", "factory": u"奥迪(进口)", "series_id": u"471", "brand_id": u"33"},
    {"factoryid": u"79", "series_name": u"奥迪A5", "brand_name": u"奥迪", "factory": u"奥迪(进口)", "series_id": u"538", "brand_id": u"33"},
    {"factoryid": u"79", "series_name": u"奥迪S5", "brand_name": u"奥迪", "factory": u"奥迪(进口)", "series_id": u"2734", "brand_id": u"33"},
    {"factoryid": u"79", "series_name": u"奥迪A6(进口)", "brand_name": u"奥迪", "factory": u"奥迪(进口)", "series_id": u"472", "brand_id": u"33"},
    {"factoryid": u"79", "series_name": u"奥迪S6", "brand_name": u"奥迪", "factory": u"奥迪(进口)", "series_id": u"2736", "brand_id": u"33"},
    {"factoryid": u"79", "series_name": u"奥迪A7", "brand_name": u"奥迪", "factory": u"奥迪(进口)", "series_id": u"740", "brand_id": u"33"},
    {"factoryid": u"79", "series_name": u"奥迪S7", "brand_name": u"奥迪", "factory": u"奥迪(进口)", "series_id": u"2738", "brand_id": u"33"},
    {"factoryid": u"79", "series_name": u"奥迪A8", "brand_name": u"奥迪", "factory": u"奥迪(进口)", "series_id": u"146", "brand_id": u"33"},
    {"factoryid": u"79", "series_name": u"奥迪S8", "brand_name": u"奥迪", "factory": u"奥迪(进口)", "series_id": u"2739", "brand_id": u"33"},
    {"factoryid": u"79", "series_name": u"奥迪Q3(进口)", "brand_name": u"奥迪", "factory": u"奥迪(进口)", "series_id": u"2264", "brand_id": u"33"},
    {"factoryid": u"79", "series_name": u"奥迪Q5(进口)", "brand_name": u"奥迪", "factory": u"奥迪(进口)", "series_id": u"593", "brand_id": u"33"},
    {"factoryid": u"79", "series_name": u"奥迪SQ5", "brand_name": u"奥迪", "factory": u"奥迪(进口)", "series_id": u"2841", "brand_id": u"33"},
    {"factoryid": u"79", "series_name": u"奥迪Q7", "brand_name": u"奥迪", "factory": u"奥迪(进口)", "series_id": u"412", "brand_id": u"33"},
    {"factoryid": u"79", "series_name": u"奥迪TT", "brand_name": u"奥迪", "factory": u"奥迪(进口)", "series_id": u"148", "brand_id": u"33"},
    {"factoryid": u"79", "series_name": u"奥迪TTS", "brand_name": u"奥迪", "factory": u"奥迪(进口)", "series_id": u"2740", "brand_id": u"33"},
    {"factoryid": u"79", "series_name": u"奥迪R8", "brand_name": u"奥迪", "factory": u"奥迪(进口)", "series_id": u"511", "brand_id": u"33"},
    {"factoryid": u"346", "series_name": u"奥迪RS 5", "brand_name": u"奥迪", "factory": u"奥迪RS", "series_id": u"2735", "brand_id": u"33"},
    {"factoryid": u"346", "series_name": u"奥迪RS 6", "brand_name": u"奥迪", "factory": u"奥迪RS", "series_id": u"2737", "brand_id": u"33"},
    {"factoryid": u"346", "series_name": u"奥迪RS 7", "brand_name": u"奥迪", "factory": u"奥迪RS", "series_id": u"2994", "brand_id": u"33"},
    {"factoryid": u"93", "series_name": u"威朗", "brand_name": u"别克", "factory": u"上汽通用别克", "series_id": u"3751", "brand_id": u"38"},
    {"factoryid": u"93", "series_name": u"英朗", "brand_name": u"别克", "factory": u"上汽通用别克", "series_id": u"982", "brand_id": u"38"},
    {"factoryid": u"93", "series_name": u"君威", "brand_name": u"别克", "factory": u"上汽通用别克", "series_id": u"164", "brand_id": u"38"},
    {"factoryid": u"93", "series_name": u"君越", "brand_name": u"别克", "factory": u"上汽通用别克", "series_id": u"834", "brand_id": u"38"},
    {"factoryid": u"93", "series_name": u"昂科拉", "brand_name": u"别克", "factory": u"上汽通用别克", "series_id": u"2896", "brand_id": u"38"},
    {"factoryid": u"93", "series_name": u"昂科威", "brand_name": u"别克", "factory": u"上汽通用别克", "series_id": u"3554", "brand_id": u"38"},
    {"factoryid": u"93", "series_name": u"别克GL8", "brand_name": u"别克", "factory": u"上汽通用别克", "series_id": u"166", "brand_id": u"38"},
    {"factoryid": u"93", "series_name": u"凯越", "brand_name": u"别克", "factory": u"上汽通用别克", "series_id": u"875", "brand_id": u"38"},
    {"factoryid": u"93", "series_name": u"林荫大道", "brand_name": u"别克", "factory": u"上汽通用别克", "series_id": u"525", "brand_id": u"38"},
    {"factoryid": u"93", "series_name": u"荣御", "brand_name": u"别克", "factory": u"上汽通用别克", "series_id": u"344", "brand_id": u"38"},
    {"factoryid": u"182", "series_name": u"昂科雷", "brand_name": u"别克", "factory": u"别克(进口)", "series_id": u"592", "brand_id": u"38"},
    {"factoryid": u"152", "series_name": u"奔驰C级", "brand_name": u"奔驰", "factory": u"北京奔驰", "series_id": u"588", "brand_id": u"36"},
    {"factoryid": u"152", "series_name": u"奔驰E级", "brand_name": u"奔驰", "factory": u"北京奔驰", "series_id": u"197", "brand_id": u"36"},
    {"factoryid": u"152", "series_name": u"奔驰GLA", "brand_name": u"奔驰", "factory": u"北京奔驰", "series_id": u"3248", "brand_id": u"36"},
    {"factoryid": u"152", "series_name": u"奔驰GLC", "brand_name": u"奔驰", "factory": u"北京奔驰", "series_id": u"3862", "brand_id": u"36"},
    {"factoryid": u"152", "series_name": u"奔驰GLK级", "brand_name": u"奔驰", "factory": u"北京奔驰", "series_id": u"2562", "brand_id": u"36"},
    {"factoryid": u"301", "series_name": u"奔驰V级", "brand_name": u"奔驰", "factory": u"福建奔驰", "series_id": u"3823", "brand_id": u"36"},
    {"factoryid": u"301", "series_name": u"威霆", "brand_name": u"奔驰", "factory": u"福建奔驰", "series_id": u"2084", "brand_id": u"36"},
    {"factoryid": u"301", "series_name": u"唯雅诺", "brand_name": u"奔驰", "factory": u"福建奔驰", "series_id": u"2034", "brand_id": u"36"},
    {"factoryid": u"301", "series_name": u"凌特", "brand_name": u"奔驰", "factory": u"福建奔驰", "series_id": u"2564", "brand_id": u"36"},
    {"factoryid": u"47", "series_name": u"奔驰A级", "brand_name": u"奔驰", "factory": u"奔驰(进口)", "series_id": u"52", "brand_id": u"36"},
    {"factoryid": u"47", "series_name": u"奔驰B级", "brand_name": u"奔驰", "factory": u"奔驰(进口)", "series_id": u"398", "brand_id": u"36"},
    {"factoryid": u"47", "series_name": u"奔驰CLA级", "brand_name": u"奔驰", "factory": u"奔驰(进口)", "series_id": u"2966", "brand_id": u"36"},
    {"factoryid": u"47", "series_name": u"奔驰C级(进口)", "brand_name": u"奔驰", "factory": u"奔驰(进口)", "series_id": u"56", "brand_id": u"36"},
    {"factoryid": u"47", "series_name": u"奔驰E级(进口)", "brand_name": u"奔驰", "factory": u"奔驰(进口)", "series_id": u"450", "brand_id": u"36"},
    {"factoryid": u"47", "series_name": u"奔驰CLS级", "brand_name": u"奔驰", "factory": u"奔驰(进口)", "series_id": u"365", "brand_id": u"36"},
    {"factoryid": u"47", "series_name": u"奔驰S级", "brand_name": u"奔驰", "factory": u"奔驰(进口)", "series_id": u"59", "brand_id": u"36"},
    {"factoryid": u"47", "series_name": u"奔驰GLE", "brand_name": u"奔驰", "factory": u"奔驰(进口)", "series_id": u"3683", "brand_id": u"36"},
    {"factoryid": u"47", "series_name": u"奔驰G级", "brand_name": u"奔驰", "factory": u"奔驰(进口)", "series_id": u"60", "brand_id": u"36"},
    {"factoryid": u"47", "series_name": u"奔驰GLS", "brand_name": u"奔驰", "factory": u"奔驰(进口)", "series_id": u"3688", "brand_id": u"36"},
    {"factoryid": u"47", "series_name": u"奔驰R级", "brand_name": u"奔驰", "factory": u"奔驰(进口)", "series_id": u"469", "brand_id": u"36"},
    {"factoryid": u"47", "series_name": u"奔驰SLK级", "brand_name": u"奔驰", "factory": u"奔驰(进口)", "series_id": u"267", "brand_id": u"36"},
    {"factoryid": u"47", "series_name": u"奔驰SL级", "brand_name": u"奔驰", "factory": u"奔驰(进口)", "series_id": u"237", "brand_id": u"36"},
    {"factoryid": u"47", "series_name": u"奔驰GLA(进口)", "brand_name": u"奔驰", "factory": u"奔驰(进口)", "series_id": u"3079", "brand_id": u"36"},
    {"factoryid": u"47", "series_name": u"Sprinter", "brand_name": u"奔驰", "factory": u"奔驰(进口)", "series_id": u"2005", "brand_id": u"36"},
    {"factoryid": u"47", "series_name": u"威霆(进口)", "brand_name": u"奔驰", "factory": u"奔驰(进口)", "series_id": u"192", "brand_id": u"36"},
    {"factoryid": u"47", "series_name": u"奔驰GLK级(进口)", "brand_name": u"奔驰", "factory": u"奔驰(进口)", "series_id": u"595", "brand_id": u"36"},
    {"factoryid": u"47", "series_name": u"奔驰M级", "brand_name": u"奔驰", "factory": u"奔驰(进口)", "series_id": u"57", "brand_id": u"36"},
    {"factoryid": u"47", "series_name": u"奔驰GL级", "brand_name": u"奔驰", "factory": u"奔驰(进口)", "series_id": u"467", "brand_id": u"36"},
    {"factoryid": u"47", "series_name": u"唯雅诺(进口)", "brand_name": u"奔驰", "factory": u"奔驰(进口)", "series_id": u"300", "brand_id": u"36"},
    {"factoryid": u"47", "series_name": u"奔驰CLK级", "brand_name": u"奔驰", "factory": u"奔驰(进口)", "series_id": u"235", "brand_id": u"36"},
    {"factoryid": u"47", "series_name": u"奔驰CL级", "brand_name": u"奔驰", "factory": u"奔驰(进口)", "series_id": u"683", "brand_id": u"36"},
    {"factoryid": u"344", "series_name": u"奔驰A级AMG", "brand_name": u"奔驰", "factory": u"梅赛德斯-AMG", "series_id": u"2842", "brand_id": u"36"},
    {"factoryid": u"344", "series_name": u"奔驰CLA级AMG", "brand_name": u"奔驰", "factory": u"梅赛德斯-AMG", "series_id": u"2967", "brand_id": u"36"},
    {"factoryid": u"344", "series_name": u"奔驰C级AMG", "brand_name": u"奔驰", "factory": u"梅赛德斯-AMG", "series_id": u"2717", "brand_id": u"36"},
    {"factoryid": u"344", "series_name": u"奔驰CLS级AMG", "brand_name": u"奔驰", "factory": u"梅赛德斯-AMG", "series_id": u"2719", "brand_id": u"36"},
    {"factoryid": u"344", "series_name": u"奔驰S级AMG", "brand_name": u"奔驰", "factory": u"梅赛德斯-AMG", "series_id": u"2197", "brand_id": u"36"},
    {"factoryid": u"344", "series_name": u"奔驰GLA AMG", "brand_name": u"奔驰", "factory": u"梅赛德斯-AMG", "series_id": u"3264", "brand_id": u"36"},
    {"factoryid": u"344", "series_name": u"奔驰GLE AMG", "brand_name": u"奔驰", "factory": u"梅赛德斯-AMG", "series_id": u"3704", "brand_id": u"36"},
    {"factoryid": u"344", "series_name": u"奔驰G级AMG", "brand_name": u"奔驰", "factory": u"梅赛德斯-AMG", "series_id": u"2723", "brand_id": u"36"},
    {"factoryid": u"344", "series_name": u"奔驰GLS AMG", "brand_name": u"奔驰", "factory": u"梅赛德斯-AMG", "series_id": u"3901", "brand_id": u"36"},
    {"factoryid": u"344", "series_name": u"奔驰SL级AMG", "brand_name": u"奔驰", "factory": u"梅赛德斯-AMG", "series_id": u"2720", "brand_id": u"36"},
    {"factoryid": u"344", "series_name": u"AMG GT", "brand_name": u"奔驰", "factory": u"梅赛德斯-AMG", "series_id": u"3451", "brand_id": u"36"},
    {"factoryid": u"344", "series_name": u"奔驰E级AMG", "brand_name": u"奔驰", "factory": u"梅赛德斯-AMG", "series_id": u"2718", "brand_id": u"36"},
    {"factoryid": u"344", "series_name": u"奔驰SLK级AMG", "brand_name": u"奔驰", "factory": u"梅赛德斯-AMG", "series_id": u"2721", "brand_id": u"36"},
    {"factoryid": u"344", "series_name": u"奔驰M级AMG", "brand_name": u"奔驰", "factory": u"梅赛德斯-AMG", "series_id": u"2722", "brand_id": u"36"},
    {"factoryid": u"344", "series_name": u"奔驰GL级AMG", "brand_name": u"奔驰", "factory": u"梅赛德斯-AMG", "series_id": u"2833", "brand_id": u"36"},
    {"factoryid": u"344", "series_name": u"奔驰SLS级AMG", "brand_name": u"奔驰", "factory": u"梅赛德斯-AMG", "series_id": u"914", "brand_id": u"36"},
    {"factoryid": u"407", "series_name": u"迈巴赫S级", "brand_name": u"奔驰", "factory": u"梅赛德斯-迈巴赫", "series_id": u"3665", "brand_id": u"36"},
    {"factoryid": u"151", "series_name": u"杰德", "brand_name": u"本田", "factory": u"东风本田", "series_id": u"3104", "brand_id": u"14"},
    {"factoryid": u"151", "series_name": u"思域", "brand_name": u"本田", "factory": u"东风本田", "series_id": u"135", "brand_id": u"14"},
    {"factoryid": u"151", "series_name": u"哥瑞", "brand_name": u"本田", "factory": u"东风本田", "series_id": u"3859", "brand_id": u"14"},
    {"factoryid": u"151", "series_name": u"思铂睿", "brand_name": u"本田", "factory": u"东风本田", "series_id": u"859", "brand_id": u"14"},
    {"factoryid": u"151", "series_name": u"本田XR-V", "brand_name": u"本田", "factory": u"东风本田", "series_id": u"3582", "brand_id": u"14"},
    {"factoryid": u"151", "series_name": u"本田CR-V", "brand_name": u"本田", "factory": u"东风本田", "series_id": u"314", "brand_id": u"14"},
    {"factoryid": u"151", "series_name": u"艾力绅", "brand_name": u"本田", "factory": u"东风本田", "series_id": u"2565", "brand_id": u"14"},
    {"factoryid": u"32", "series_name": u"飞度", "brand_name": u"本田", "factory": u"广汽本田", "series_id": u"81", "brand_id": u"14"},
    {"factoryid": u"32", "series_name": u"锋范", "brand_name": u"本田", "factory": u"广汽本田", "series_id": u"3876", "brand_id": u"14"},
    {"factoryid": u"32", "series_name": u"凌派", "brand_name": u"本田", "factory": u"广汽本田", "series_id": u"3085", "brand_id": u"14"},
    {"factoryid": u"32", "series_name": u"歌诗图", "brand_name": u"本田", "factory": u"广汽本田", "series_id": u"2168", "brand_id": u"14"},
    {"factoryid": u"32", "series_name": u"雅阁", "brand_name": u"本田", "factory": u"广汽本田", "series_id": u"78", "brand_id": u"14"},
    {"factoryid": u"32", "series_name": u"缤智", "brand_name": u"本田", "factory": u"广汽本田", "series_id": u"3460", "brand_id": u"14"},
    {"factoryid": u"32", "series_name": u"奥德赛", "brand_name": u"本田", "factory": u"广汽本田", "series_id": u"880", "brand_id": u"14"},
    {"factoryid": u"32", "series_name": u"锋范经典", "brand_name": u"本田", "factory": u"广汽本田", "series_id": u"694", "brand_id": u"14"},
    {"factoryid": u"32", "series_name": u"思迪", "brand_name": u"本田", "factory": u"广汽本田", "series_id": u"449", "brand_id": u"14"},
    {"factoryid": u"75", "series_name": u"INSIGHT", "brand_name": u"本田", "factory": u"本田(进口)", "series_id": u"723", "brand_id": u"14"},
    {"factoryid": u"75", "series_name": u"本田CR-Z", "brand_name": u"本田", "factory": u"本田(进口)", "series_id": u"897", "brand_id": u"14"},
    {"factoryid": u"75", "series_name": u"飞度(进口)", "brand_name": u"本田", "factory": u"本田(进口)", "series_id": u"900", "brand_id": u"14"},
    {"factoryid": u"75", "series_name": u"里程", "brand_name": u"本田", "factory": u"本田(进口)", "series_id": u"231", "brand_id": u"14"},
    {"factoryid": u"75", "series_name": u"时韵", "brand_name": u"本田", "factory": u"本田(进口)", "series_id": u"233", "brand_id": u"14"},
    {"factoryid": u"176", "series_name": u"马自达3 Axela昂克赛拉", "brand_name": u"马自达", "factory": u"长安马自达", "series_id": u"3294", "brand_id": u"58"},
    {"factoryid": u"176", "series_name": u"马自达3星骋", "brand_name": u"马自达", "factory": u"长安马自达", "series_id": u"2418", "brand_id": u"58"},
    {"factoryid": u"176", "series_name": u"马自达CX-5", "brand_name": u"马自达", "factory": u"长安马自达", "series_id": u"2987", "brand_id": u"58"},
    {"factoryid": u"176", "series_name": u"马自达2", "brand_name": u"马自达", "factory": u"长安马自达", "series_id": u"433", "brand_id": u"58"},
    {"factoryid": u"176", "series_name": u"马自达2劲翔", "brand_name": u"马自达", "factory": u"长安马自达", "series_id": u"641", "brand_id": u"58"},
    {"factoryid": u"176", "series_name": u"马自达3", "brand_name": u"马自达", "factory": u"长安马自达", "series_id": u"363", "brand_id": u"58"},
    {"factoryid": u"11", "series_name": u"阿特兹", "brand_name": u"马自达", "factory": u"一汽马自达", "series_id": u"3154", "brand_id": u"58"},
    {"factoryid": u"11", "series_name": u"马自达6", "brand_name": u"马自达", "factory": u"一汽马自达", "series_id": u"22", "brand_id": u"58"},
    {"factoryid": u"11", "series_name": u"睿翼", "brand_name": u"马自达", "factory": u"一汽马自达", "series_id": u"655", "brand_id": u"58"},
    {"factoryid": u"11", "series_name": u"马自达CX-4", "brand_name": u"马自达", "factory": u"一汽马自达", "series_id": u"3968", "brand_id": u"58"},
    {"factoryid": u"11", "series_name": u"马自达CX-7", "brand_name": u"马自达", "factory": u"一汽马自达", "series_id": u"3066", "brand_id": u"58"},
    {"factoryid": u"11", "series_name": u"马自达8", "brand_name": u"马自达", "factory": u"一汽马自达", "series_id": u"2118", "brand_id": u"58"},
    {"factoryid": u"119", "series_name": u"马自达5", "brand_name": u"马自达", "factory": u"马自达(进口)", "series_id": u"578", "brand_id": u"58"},
    {"factoryid": u"119", "series_name": u"马自达MX-5", "brand_name": u"马自达", "factory": u"马自达(进口)", "series_id": u"672", "brand_id": u"58"},
    {"factoryid": u"119", "series_name": u"马自达CX-9", "brand_name": u"马自达", "factory": u"马自达(进口)", "series_id": u"1005", "brand_id": u"58"},
    {"factoryid": u"119", "series_name": u"马自达3(进口)", "brand_name": u"马自达", "factory": u"马自达(进口)", "series_id": u"584", "brand_id": u"58"},
    {"factoryid": u"119", "series_name": u"ATENZA", "brand_name": u"马自达", "factory": u"马自达(进口)", "series_id": u"3096", "brand_id": u"58"},
    {"factoryid": u"119", "series_name": u"马自达CX-5(进口)", "brand_name": u"马自达", "factory": u"马自达(进口)", "series_id": u"2391", "brand_id": u"58"},
    {"factoryid": u"119", "series_name": u"马自达CX-7(进口)", "brand_name": u"马自达", "factory": u"马自达(进口)", "series_id": u"658", "brand_id": u"58"},
    {"factoryid": u"119", "series_name": u"马自达8(进口)", "brand_name": u"马自达", "factory": u"马自达(进口)", "series_id": u"304", "brand_id": u"58"},
    {"factoryid": u"119", "series_name": u"马自达RX-8", "brand_name": u"马自达", "factory": u"马自达(进口)", "series_id": u"295", "brand_id": u"58"},
    {"factoryid": u"29", "series_name": u"宝马2系旅行车", "brand_name": u"宝马", "factory": u"华晨宝马", "series_id": u"3941", "brand_id": u"15"},
    {"factoryid": u"29", "series_name": u"宝马3系", "brand_name": u"宝马", "factory": u"华晨宝马", "series_id": u"66", "brand_id": u"15"},
    {"factoryid": u"29", "series_name": u"宝马5系", "brand_name": u"宝马", "factory": u"华晨宝马", "series_id": u"65", "brand_id": u"15"},
    {"factoryid": u"29", "series_name": u"宝马X1", "brand_name": u"宝马", "factory": u"华晨宝马", "series_id": u"2561", "brand_id": u"15"},
    {"factoryid": u"80", "series_name": u"宝马i3", "brand_name": u"宝马", "factory": u"宝马(进口)", "series_id": u"2388", "brand_id": u"15"},
    {"factoryid": u"80", "series_name": u"宝马1系(进口)", "brand_name": u"宝马", "factory": u"宝马(进口)", "series_id": u"373", "brand_id": u"15"},
    {"factoryid": u"80", "series_name": u"宝马3系(进口)", "brand_name": u"宝马", "factory": u"宝马(进口)", "series_id": u"317", "brand_id": u"15"},
    {"factoryid": u"80", "series_name": u"宝马3系GT", "brand_name": u"宝马", "factory": u"宝马(进口)", "series_id": u"2963", "brand_id": u"15"},
    {"factoryid": u"80", "series_name": u"宝马4系", "brand_name": u"宝马", "factory": u"宝马(进口)", "series_id": u"2968", "brand_id": u"15"},
    {"factoryid": u"80", "series_name": u"宝马5系(进口)", "brand_name": u"宝马", "factory": u"宝马(进口)", "series_id": u"202", "brand_id": u"15"},
    {"factoryid": u"80", "series_name": u"宝马5系GT", "brand_name": u"宝马", "factory": u"宝马(进口)", "series_id": u"2847", "brand_id": u"15"},
    {"factoryid": u"80", "series_name": u"宝马6系", "brand_name": u"宝马", "factory": u"宝马(进口)", "series_id": u"270", "brand_id": u"15"},
    {"factoryid": u"80", "series_name": u"宝马7系", "brand_name": u"宝马", "factory": u"宝马(进口)", "series_id": u"153", "brand_id": u"15"},
    {"factoryid": u"80", "series_name": u"宝马X3", "brand_name": u"宝马", "factory": u"宝马(进口)", "series_id": u"271", "brand_id": u"15"},
    {"factoryid": u"80", "series_name": u"宝马X4", "brand_name": u"宝马", "factory": u"宝马(进口)", "series_id": u"3053", "brand_id": u"15"},
    {"factoryid": u"80", "series_name": u"宝马X5", "brand_name": u"宝马", "factory": u"宝马(进口)", "series_id": u"159", "brand_id": u"15"},
    {"factoryid": u"80", "series_name": u"宝马X6", "brand_name": u"宝马", "factory": u"宝马(进口)", "series_id": u"587", "brand_id": u"15"},
    {"factoryid": u"80", "series_name": u"宝马2系多功能旅行车", "brand_name": u"宝马", "factory": u"宝马(进口)", "series_id": u"3726", "brand_id": u"15"},
    {"factoryid": u"80", "series_name": u"宝马2系", "brand_name": u"宝马", "factory": u"宝马(进口)", "series_id": u"3230", "brand_id": u"15"},
    {"factoryid": u"80", "series_name": u"宝马i8", "brand_name": u"宝马", "factory": u"宝马(进口)", "series_id": u"2387", "brand_id": u"15"},
    {"factoryid": u"80", "series_name": u"宝马Z4", "brand_name": u"宝马", "factory": u"宝马(进口)", "series_id": u"161", "brand_id": u"15"},
    {"factoryid": u"80", "series_name": u"宝马2系旅行车(进口)", "brand_name": u"宝马", "factory": u"宝马(进口)", "series_id": u"3302", "brand_id": u"15"},
    {"factoryid": u"80", "series_name": u"宝马X1(进口)", "brand_name": u"宝马", "factory": u"宝马(进口)", "series_id": u"675", "brand_id": u"15"},
    {"factoryid": u"345", "series_name": u"宝马M3", "brand_name": u"宝马", "factory": u"宝马M", "series_id": u"2196", "brand_id": u"15"},
    {"factoryid": u"345", "series_name": u"宝马M4", "brand_name": u"宝马", "factory": u"宝马M", "series_id": u"3189", "brand_id": u"15"},
    {"factoryid": u"345", "series_name": u"宝马M5", "brand_name": u"宝马", "factory": u"宝马M", "series_id": u"2726", "brand_id": u"15"},
    {"factoryid": u"345", "series_name": u"宝马M6", "brand_name": u"宝马", "factory": u"宝马M", "series_id": u"2727", "brand_id": u"15"},
    {"factoryid": u"345", "series_name": u"宝马X5 M", "brand_name": u"宝马", "factory": u"宝马M", "series_id": u"2728", "brand_id": u"15"},
    {"factoryid": u"345", "series_name": u"宝马X6 M", "brand_name": u"宝马", "factory": u"宝马M", "series_id": u"2729", "brand_id": u"15"},
    {"factoryid": u"345", "series_name": u"宝马M2", "brand_name": u"宝马", "factory": u"宝马M", "series_id": u"3357", "brand_id": u"15"},
    {"factoryid": u"345", "series_name": u"宝马1系M", "brand_name": u"宝马", "factory": u"宝马M", "series_id": u"2725", "brand_id": u"15"}
]

PAGE_SIZE = 24

class Che168Rank(CrawlSpider):
    name = 'che168_rank'

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
                for city in crawling_cities:
                    for series in crawling_series:
                        url_prefix = 'https://appsapi.che168.com/Phone/V57/cars/search.ashx?_appid=2scapp.ios&appversion=5.5.9&channelid=App Store&cid=%s&cpcnum=4&dealertype=9&ispic=0&orderby=0&pagesize=%s&pid=%s&seriesid=%s&brandid=%s&_sign=cda602a1e47e463968fdbe03a58f04a3' % (city['city_id'], PAGE_SIZE, city['province_id'], series['series_id'], series['brand_id'])
                        yield Request('%s&pageindex=%s' % (url_prefix, page), meta={'url_prefix': url_prefix, 'type': 'get_cars_info', 'page': page, 'city_name': city['name']}, dont_filter=True)
            elif self.category == 'price':
                for city in crawling_cities:
                    for price in crawling_price:
                        url_prefix = 'https://appsapi.che168.com/Phone/V57/cars/search.ashx?_appid=2scapp.ios&appversion=5.5.9&channelid=App Store&cid=%s&cpcnum=4&dealertype=9&ispic=0&orderby=0&pagesize=%s&pid=%s&priceregion=%s&_sign=cda602a1e47e463968fdbe03a58f04a3' % (city['city_id'], PAGE_SIZE, city['province_id'], price)
                        yield Request('%s&pageindex=%s' % (url_prefix, page), meta={'url_prefix': url_prefix, 'type': 'get_cars_info', 'page': page, 'city_name': city['name']}, dont_filter=True)
            else:
                for city in crawling_cities:
                    url_prefix = 'https://appsapi.che168.com/Phone/V57/cars/search.ashx?_appid=2scapp.ios&appversion=5.5.9&channelid=App Store&cid=%s&cpcnum=4&dealertype=9&ispic=0&orderby=0&pagesize=%s&pid=%s&_sign=cda602a1e47e463968fdbe03a58f04a3' % (city['city_id'], PAGE_SIZE, city['province_id'])
                    yield Request('%s&pageindex=%s' % (url_prefix, page), meta={'url_prefix': url_prefix, 'type': 'get_cars_info', 'page': page, 'city_name': city['name']}, dont_filter=True)

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
                ri.ranking = json.dumps({int(time.time()): i + 1 + (response.meta['page'] - 1) * PAGE_SIZE})  # cause ranking start from 1 while list indices start from 0
                mi = ModelItem()
                mi['model'] = [ri]
                yield mi


if __name__ == '__main__':
    execute('scrapy crawl che168_rank -a category=series'.split(' '))
