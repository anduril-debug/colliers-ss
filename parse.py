from scrapy.crawler import CrawlerProcess
from spider_links import FlatLinksSpider
from spider_items import FlatSpider



process = CrawlerProcess()
process.crawl(FlatLinksSpider)
process.crawl(FlatSpider)
process.start()
