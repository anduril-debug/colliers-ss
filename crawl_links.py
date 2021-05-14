from scrapy.crawler import CrawlerProcess
from spiders.FlatLinkSpider import FlatLinkSpider
from spiders.HouseLinkSpider import HouseLinkSpider

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging


configure_logging()
runner = CrawlerRunner()
runner.crawl(FlatLinkSpider)
runner.crawl(HouseLinkSpider)
d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run()
