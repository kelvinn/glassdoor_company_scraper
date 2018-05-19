# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import Rule

class GlassdoorSpider(scrapy.Spider):
    name = 'glassdoor'
    allowed_domains = ['glassdoor.com', 'www.glassdoor.com', 'www.glassdoor.com.au']
    start_urls = ['https://www.glassdoor.com']

    rules = [
        Rule(LinkExtractor(allow=r'\/Reviews\/.*'), callback='parse', follow=True)
    ]

    def start_requests(self):
        urls = [
            'https://www.glassdoor.com.au/Reviews/sydney-reviews-SRCH_IL.0,6_IM962.htm',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for company in response.css('div.eiHdrModule'):
            yield {
                'name': company.css("a.tightAll::text").extract_first().strip(),
                'score': company.css("span.bigRating::text").extract_first(),
                'reviews': company.css("span.num::text")[0].extract().strip(),
                'salaries': company.css("span.num::text")[1].extract().strip(),
                'interviews': company.css("span.num::text")[2].extract().strip(),
            }

        for href in response.css('li.page a::attr(href)'):
            yield response.follow(href, callback=self.parse)