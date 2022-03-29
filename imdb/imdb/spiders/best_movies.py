# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[1]")),
    )

    def parse_item(self, response):
        yield{
            'title': response.xpath('//div[@class="sc-94726ce4-2 khmuXj"]/h1/text()').get(),

            'year': response.xpath("(//a[@class='ipc-link ipc-link--baseAlt ipc-link--inherit-color sc-52284603-1 ifnKcw'])[1]/text()").get(),

            'duration': response.xpath("(//ul[@class='ipc-inline-list ipc-inline-list--show-dividers sc-52284603-0 blbaZJ baseAlt']/li[3]/text())[1]").get() + response.xpath("(//ul[@class='ipc-inline-list ipc-inline-list--show-dividers sc-52284603-0 blbaZJ baseAlt']/li[3]/text())[2]").get() + ":" + response.xpath("(//ul[@class='ipc-inline-list ipc-inline-list--show-dividers sc-52284603-0 blbaZJ baseAlt']/li[3]/text())[4]").get() + response.xpath("(//ul[@class='ipc-inline-list ipc-inline-list--show-dividers sc-52284603-0 blbaZJ baseAlt']/li[3]/text())[5]").get(),

            'genre': response.xpath("//div[@class='ipc-chip-list sc-16ede01-4 bMBIRz']/a/span/text()").getall(),

            'rating': response.xpath("(//div[@class='sc-7ab21ed2-2 kYEdvH']/span[@class='sc-7ab21ed2-1 jGRxWM'])[1]/text()").get(),

            'movie_url': response.url
        }
