# -*- coding: utf-8 -*-
import scrapy
from craigslistnby.items import CraigslistnbyItem

class CraigslistSpider(scrapy.Spider):
    name = 'rentcrawl'
    allowed_domains = ['sfbay.craigslist.org']
    start_urls = ['https://sfbay.craigslist.org/d/apts-housing-for-rent/search/nby/apa',]
    custom_settings = {
	'FEED_EXPORT_FIELDS': ["rent", "detail", "title", "desc", "url"],
	}

    def parse(self, response):
        for href in response.css('a.result-title.hdrlnk::attr(href)'):
        	url = response.urljoin(href.extract())
        	yield scrapy.Request(url, callback=self.parse_detail_page)
        	print("URL is",url)

    def parse_detail_page(self, response):
        rental = CraigslistnbyItem()
        rental['rent'] = response.css('span.price::text').extract_first()
        rental['detail'] = response.css('span.housing::text').extract_first()
        rental['title'] = response.css('span#titletextonly::text').extract_first()
        rental['desc'] = response.css('section#postingbody::text').extract()[1].strip()
        rental['url'] = response.url
        yield rental