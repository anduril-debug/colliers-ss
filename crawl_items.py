from scrapy.crawler import CrawlerProcess
from spiders.FlatSpider import FlatSpider
from spiders.HouseSpider import HouseSpider

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging


configure_logging()
runner = CrawlerRunner()
runner.crawl(FlatSpider)
runner.crawl(HouseSpider)
d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run()
