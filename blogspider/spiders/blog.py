import scrapy
from blogspider.items import BlogspiderItem


class BlogSpider(scrapy.Spider):
    name = "blog"
    allowed_domains = ['github.io']
    base_url = 'http://shaoyikai.github.io'

    def start_requests(self):
        yield scrapy.Request('http://shaoyikai.github.io', self.parse)

    def parse(self,response):
        item = BlogspiderItem()

        for row in response.xpath('//div[@class="page clearfix"]/div[@class="left"]/ul/li'):
            content_url = self.base_url + row.xpath('h2/a/@href').extract_first()
            item['title'] = row.xpath('h2/a/text()').extract_first()
            yield scrapy.Request(url=content_url, meta={'item': item}, callback=self.parse_content, dont_filter=False)

        next_page = response.xpath('//div[@class="pagination"]/a[@class="next"][1]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(self.base_url + next_page)
            yield scrapy.Request(next_page, callback=self.parse, dont_filter=False)

    def parse_content(self, response):
        item = response.meta['item']
        item['content'] = response.xpath('/html/body/div[1]/div[1]/article').extract_first()
        yield item
