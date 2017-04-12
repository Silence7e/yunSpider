# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DoubanMovieItem(scrapy.Item):
    # 排名
    ranking = scrapy.Field()
    # 电影名称
    movie_name = scrapy.Field()
    # 评分
    score = scrapy.Field()
    # 评论人数
    score_num = scrapy.Field()


class PlayListItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()


class SongItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    singer = scrapy.Field()
    singer_id = scrapy.Field()


class CommentItem(scrapy.Item):
    id = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
    user_name = scrapy.Field()
    user_id = scrapy.Field()
