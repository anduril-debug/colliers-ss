from scrapy.crawler import CrawlerProcess
from spider_links import FlatLinksSpider
from spider_items import FlatSpider




def parse_flat_links():
    print("STARTING SCRAPING FLAT LINKS....")


    process = CrawlerProcess()
    process.crawl(FlatLinksSpider)
    process.start()


def parse_flats():
    print("STARTING SCRAPING FLATS....")


    process = CrawlerProcess()
    process.crawl(FlatSpider)
    process.start()



# parse_flat_links()
# print("FINISHED FLAT LINKS PARSING....")
# print("STARTED FLATS PARSING>>>>")
parse_flats()
