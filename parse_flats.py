from scrapy.crawler import CrawlerProcess
from spider_items import FlatSpider

process = CrawlerProcess()
process.crawl(FlatSpider)
process.start()
