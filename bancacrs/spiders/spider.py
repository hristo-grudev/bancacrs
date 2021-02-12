import scrapy

from scrapy.loader import ItemLoader
from ..items import BancacrsItem
from itemloaders.processors import TakeFirst


class BancacrsSpider(scrapy.Spider):
	name = 'bancacrs'
	start_urls = ['https://bancacrs.it/news/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="read-more"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//div[@class="contenuti-header-bold-news-rassegna-stampa-dettaglio"]/text()').get()
		description = response.xpath('//div[@class="col-xs-12"][@style="paddijng-right; 0px; padding-left: 0px;"]//text()[normalize-space() and not(ancestor::noscript | ancestor::div[@class="contenuti-header-bold-news-rassegna-stampa-dettaglio"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('(//div[@class="contenuti-testo-news-rassegna-stampa"]/p/text())[1]').get()

		item = ItemLoader(item=BancacrsItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
