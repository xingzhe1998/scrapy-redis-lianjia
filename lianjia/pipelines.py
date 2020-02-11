# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import datetime
import pymongo
from scrapy.exceptions import DropItem

# from lianjia.settings import MONGO_URI,MONGO_DB


class LianjiaPipeline(object):

    def process_item(self, item, spider):
        # fmt = '%m月%d日'
        # r_date = item['r_date']
        # search = re.search(r'(\d+)\w+', r_date)
        # if search:
        #     dif_date = search.group(1)
        #     real_date = datetime.date.today()-datetime.timedelta(int(dif_date)+1)
        #     item['r_date'] = real_date.strftime(fmt)
        # else:
        #     item['r_date'] = datetime.date.today().strftime(fmt)
        # # 转成json字符串
        # # print('json格式转换之前...',type(item)) # <class 'lianjia.items.LianjiaItem'>
        # # item = json.dumps(dict(item), ensure_ascii=False)
        # # print('json格式转换之后...', type(item)) # <class 'str'>
        # # except Exception:
        # #     raise DropItem('数据丢失...')
        # print(dict(item))
        return item

class MonogoPipline(object):

    collection_name = 'rent_info'           # 表名

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        print('正在插入mongodb...')
        self.db[self.collection_name].insert_one(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
