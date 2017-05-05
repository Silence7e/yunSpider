# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#import pymongo
import json
import psycopg2
# from scrapy.conf import settings

class ScrapyspiderPipeline(object):
    def __init__(self):
        self.ids = set()
        # 链接数据库
        # self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # 数据库登录需要帐号密码的话
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        # self.db = self.client[settings['MONGO_DB']]  # 获得数据库的句柄
        # self.coll = self.db[settings['MONGO_COLL']]  # 获得collection的句柄
        # self.conn = psycopg2.connect(database="ykestate", user="ykestate", password="ykestate", host="139.196.34.70", port="5432")
        # self.cur = self.conn.cursor()
        # self.cur.execute("""select * from t_district where city_id = 1 order by id""")
        # rows = self.cur.fetchall()
        # for i in rows:
        #     print(i)

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
