import scrapy
from scrapy.crawler import CrawlerProcess

class MySpider1(scrapy.Spider):
    name = "test"
    start_urls = [
        'https://ss.ge/ka/udzravi-qoneba/iyideba-mitsis-nakveti-abashashi-3877911',
    ]

    def parse(self, response):
        info = response.css("div.detailed_page_navlist")
        ul = info.css("ul")
        lis = ul.css("li")
        a = lis.css("a::text")

        for i in a[3:]:
            print("###")
            print(i.get().strip())

process = CrawlerProcess()
process.crawl(MySpider1)
process.start()
