import scrapy
import os
import json
from flatten_json import flatten


class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["alpinetrek.co.uk"]
    start_urls = ["https://www.alpinetrek.co.uk/outdoor-clothing/for--men/1/"]

    def parse(self, response):
        links = response.css('a.product-link')
        yield from response.follow_all(
            links, callback=self.parse_item) # meta={'proxy': os.getenv("proxy")}

        # this goes through every page of the site
        pagination = response.css('div[data-codecept="pagination"] a')
        yield from response.follow_all(
            pagination, callback=self.parse)

    def parse_item(self, response):
        script_tag = response.css('script[type="application/ld+json"]')  # this is a list of dictionaries
        for script in script_tag:
            data = json.loads(script.css('::text').get())
            for item in data:
                if 'offers' in item:
                    yield flatten(dict(item))



