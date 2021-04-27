from scrapy.crawler import CrawlerProcess
from spiders import FlatLinksSpider


process = CrawlerProcess()
process.crawl(FlatLinksSpider)
process.start()
