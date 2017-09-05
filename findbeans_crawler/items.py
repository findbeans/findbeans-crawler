# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FindbeansCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    rank = scrapy.Field()
    title = scrapy.Field()
    rating = scrapy.Field()
    director = scrapy.Field()
    description = scrapy.Field()
    actors = scrapy.Field()
    posters = scrapy.Field()

