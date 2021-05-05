from scrapy.crawler import CrawlerProcess
from spider_links import FlatLinksSpider

process = CrawlerProcess()
process.crawl(FlatLinksSpider)
process.start()
