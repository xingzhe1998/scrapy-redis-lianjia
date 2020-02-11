# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    r_city = scrapy.Field()
    r_locate = scrapy.Field()
    r_url = scrapy.Field()
    r_img_url = scrapy.Field()
    r_title = scrapy.Field()
    r_info = scrapy.Field()
    r_date = scrapy.Field()
    r_price = scrapy.Field()
    r_tags = scrapy.Field()
    r_lng = scrapy.Field()  # 经度
    r_lat = scrapy.Field()  # 纬度
