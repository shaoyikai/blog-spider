import scrapy
from blogspider.items import BlogspiderItem

class BlogSpider(scrapy.Spider):
    name = "blog"
    allowed_domains = ['github.io']
    base_url = 'http://shaoyikai.github.io'
    start_urls = ['http://shaoyikai.github.io']

    def parse(self, response):
        item = BlogspiderItem()

        for row in response.xpath('//div[@class="page clearfix"]/div[@class="left"]/ul/li'):
            item['title'] = row.xpath('h2/a/text()').extract_first()
            item['content'] = row.xpath('div[@class="excerpt"]/text()').extract_first()
            yield item

        next_page = response.xpath('//div[@class="pagination"]/a[@class="next"][1]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(self.base_url + next_page)
            yield scrapy.Request(next_page, callback=self.parse)