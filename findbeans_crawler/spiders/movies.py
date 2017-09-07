# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider

from findbeans_crawler.items import FindbeansCrawlerItem


class MoviesSpider(CrawlSpider):
    name = 'movies'
    allowed_domains = ['www.imdb.com']
    start_urls = [
        'http://www.imdb.com/chart/top?ref_=nv_mv_250_6',
    ]

    def parse(self, response):
        i = 0
        for href in response.xpath('//tbody[@class="lister-list"]/tr/td[@class="posterColumn"]/a/@href'):
            if i < 20:
                i = i + 1
                url = response.urljoin(href.extract())
                yield scrapy.Request(url, callback=self.parse_item)
            else:
                return

    def parse_item(self, response):
        item = FindbeansCrawlerItem()
        item['rank'] = int(response.xpath('//div[@id="titleAwardsRanks"]/strong/a/text()').re(r'[\s\w]*#(\d+)')[0])
        item['title'] = response.xpath('//div[@class="title_wrapper"]/h1/text()').extract_first().strip()
        item['rating'] = response.xpath('//div[@class="ratingValue"]/strong/span/text()').extract_first()
        item['director'] = response.xpath('//span[@itemprop="director"]/a/span/text()').extract_first()
        item['description'] = response.xpath('//div[@id="titleStoryLine"]/div[@itemprop="description"]/p/text()').extract_first().strip().replace('\n', '')
        item['actors'] = response.xpath('//span[@itemprop="actors"]/a/span/text()').extract()
        item['posters'] = [response.xpath('//div[@class="poster"]/a/img/@src').extract_first()]
        poster_url = response.urljoin(response.xpath('//div[@class="poster"]/a/@href').extract_first())
        yield scrapy.Request(poster_url, meta={'item': item}, callback=self.parse_poster_urls)

    def parse_poster_urls(self, response):
        item = response.meta['item']
        posters = response.xpath('//script/text()').re("\"src\":\"(https:[\/\w\-\.\,@]*)\"")[:4]
        for poster in posters:
            item['posters'].append(poster)
        yield item


# process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
# process = CrawlerProcess(get_project_settings())
# process.crawl(MoviesSpider)
# process.start()
