# coding:utf8
import datetime

from ISpider.model.NewsModel import WholeNetworkNews

__author__ = 'pangguangde'


def get_recent_news(site):
    h_time = datetime.datetime.now()
    # l_time = datetime.datetime(2017, 1, 22, 10, 57, 0)
    l_time = datetime.datetime.now() - datetime.timedelta(days=7)
    return [
        item for item in WholeNetworkNews.select().where(
            WholeNetworkNews.site == site,
            WholeNetworkNews.clue_id.is_null(False),
            WholeNetworkNews.created_time.between(l_time, h_time)
        ).execute()
    ]

if __name__ == '__main__':
    data = get_recent_news('163')
    print len('163')
