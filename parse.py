from scrapy.crawler import CrawlerProcess
from spider_links import FlatLinksSpider,HouseLinkSpider
from spider_items import FlatSpider,HouseSpider




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



def parse_house_links():
    print("STARTING SCRAPING HOUSE LINKS....")

    process = CrawlerProcess()
    process.crawl(HouseLinkSpider)
    process.start()


def parse_house():
    print("STARTING SCRAPING HOUSE LINKS....")

    process = CrawlerProcess()
    process.crawl(HouseSpider)
    process.start()




# parse_flat_links()
# parse_flats()
# parse_house_links()
parse_house()
