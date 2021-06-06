from scrapy.crawler import CrawlerProcess
from spiders.FlatRemodelSpider import FlatRemodelSpider
from spiders.HouseRemodelSpider import HouseRemodelSpider

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging


configure_logging()
runner = CrawlerRunner()
runner.crawl(FlatRemodelSpider)
runner.crawl(HouseRemodelSpider)
d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run()
