# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#import pymongo
import json
# from scrapy.conf import settings

class ScrapyspiderPipeline(object):
    def __init__(self):
        self.ids = set();
        # 链接数据库
        # self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # 数据库登录需要帐号密码的话
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        # self.db = self.client[settings['MONGO_DB']]  # 获得数据库的句柄
        # self.coll = self.db[settings['MONGO_COLL']]  # 获得collection的句柄

    def process_item(self, item, spider):
        postItem = dict(item)  # 把item转化成字典形式
        list = postItem['list']
        new_list = []
        for u in list:
            new_list.append(dict(u))
        postItem['list'] = new_list
        # self.coll.insert(postItem)  # 向数据库插入一条记录

        json_str =json.dumps(postItem)
        return item
