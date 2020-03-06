# -*- coding: utf-8 -*-
import scrapy


class CollectionSpider(scrapy.Spider):
    name = 'collection'
    allowed_domains = ["pstrial-2019-12-16.toscrape.com"]
    page = 1
    start_urls = ["http://pstrial-2019-12-16.toscrape.com"]


    def parse(self, response):
        next_page_url = response.css("a::attr('href')").extract()[1]
        next_page_url = response.urljoin(next_page_url)
        if next_page_url:
        	yield scrapy.Request(url=next_page_url, callback=self.browse_page)


    def browse_page(self, response):
    	insunsh_page_url = response.css('a::attr("href")').re('/browse/insunsh')
    	summertime_page_url = response.css('a::attr("href")').re('/browse/summertime/wrapperfrom')[0]
    	insunsh_page_url = ''.join(insunsh_page_url)
    	insunsh_page_url = response.urljoin(insunsh_page_url)
    	summertime_page_url = ''.join(summertime_page_url)
    	summertime_page_url = response.urljoin(summertime_page_url)
    	if insunsh_page_url:
    		yield scrapy.Request(url=insunsh_page_url, callback=self.insunsh_pagination)
    	if summertime_page_url:
    		yield scrapy.Request(url=summertime_page_url, callback=self.barnowl_page)



    def insunsh_pagination(self, response):
    	total_page_count = self.total_page_count(response)
    	pagination_urls = ['http://pstrial-2019-12-16.toscrape.com/browse/insunsh?page=%s' % page for page in range(0,total_page_count)]
    	print(pagination_urls)
    	for next_page in pagination_urls:
    		yield scrapy.Request(url=next_page, callback=self.parse_listings)


    def parse_listings(self, response):
    	detail_page_links = response.xpath('//a[contains(@href, "item")]/@href').extract()
    	for detail_page in detail_page_links:
    		detail_page_url = response.urljoin(detail_page)
    		yield scrapy.Request(url=detail_page_url, callback=self.fetch_item_details)


    def fetch_item_details(self, response):
    	page_url = response.url
    	artist = response.css('#content > h2.artist::text').get()
    	title = response.css('#content > h1::text').get()
    	image_url = ''.join(response.xpath('//img/@src').extract())
    	image_url = response.urljoin(image_url)
    	description = response.css("#content > div.description > p::text").get()
    	tags = response.css('#content > a::attr("href")').get()
    	tags = tags.split("/")[1: ]
    	yield {
    		"url": page_url,
    		"artist": artist,
    		"title": title,
    		"image_url": image_url,
    		"description": description,
    		"tags": tags
    	}


    def barnowl_page(self, response):
    	barnowl_page_url = response.css("a::attr('href')").re('/browse/summertime/wrapperfrom/barnowl')[0]
    	barnowl_page_url = response.urljoin(barnowl_page_url)
    	if barnowl_page_url:
    		yield scrapy.Request(url=barnowl_page_url, callback=self.barnowl_pagination)


    def barnowl_pagination(self, response):
    	total_page_count = self.total_page_count(response)
    	pagination_urls = ["http://pstrial-2019-12-16.toscrape.com/browse/summertime/wrapperfrom/barnowl?page=%s" 
    	% page for page in range(0,total_page_count)]
    	for page_url in pagination_urls:
    		yield scrapy.Request(url=page_url, callback=self.parse_listings)


    def total_page_count(self, response):
    	total_items=response.css("label.item-count::text").get().split()[0]
    	total_items=int(total_items)
    	total_page_count = int(total_items/10)
    	return total_page_count






