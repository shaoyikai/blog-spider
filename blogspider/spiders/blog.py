import scrapy

class BlogSpider(scrapy.Spider):
    name = "blog"
    base_url = 'http://shaoyikai.github.io'
    start_urls = ['http://shaoyikai.github.io']

    def parse(self, response):

        for row in response.xpath('//div[@class="page clearfix"]/div[@class="left"]/ul/li'):
            yield {
                'title': row.xpath('h2/a/text()').extract_first(),
                'content': row.xpath('div[@class="excerpt"]/text()').extract_first(),
            }

        next_page = response.xpath('//div[@class="pagination"]/a[@class="next"][1]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(self.base_url + next_page)
            yield scrapy.Request(next_page, callback=self.parse)