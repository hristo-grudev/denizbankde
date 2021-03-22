import scrapy

from scrapy.loader import ItemLoader

from ..items import DenizbankdeItem
from itemloaders.processors import TakeFirst


class DenizbankdeSpider(scrapy.Spider):
	name = 'denizbankde'
	start_urls = ['https://www.denizbank.de/de/%C3%9CberUns/PresseCenter/']

	def parse(self, response):
		post_links = response.xpath('//a[text()="Mehr Info"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//div[@class="content"]//h2/text()|//div[@class="content"]//h1/text()').get()
		description = response.xpath('//div[@class="content"]//text()[normalize-space() and not(ancestor::h2 | ancestor::h1)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=DenizbankdeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
