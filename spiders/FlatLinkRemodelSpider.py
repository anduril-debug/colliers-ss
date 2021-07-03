import scrapy
from items import LinkItem
from pipelines_remodel import FlatLinkRemodelPipeline
from datetime import datetime
import requests

import requests
from bs4 import BeautifulSoup


#findind last page
URL = "https://ss.ge/ka/udzravi-qoneba/l/bina/iyideba?Page=1&RealEstateTypeId=5&RealEstateDealTypeId=4&StatusField.FieldId=34&StatusField.Type=SingleSelect&StatusField.StandardField=Status&PriceType=false&CurrencyId=1"
response = requests.get(URL)

soup = BeautifulSoup(response.content,'html.parser')
buttons = soup.find('div', class_="latest_all_adds")
last_li = buttons.find('li', "last")

pagination = int(last_li.a.text)+1


class FlatLinkRemodelSpider(scrapy.Spider):

    name = "flat_links"
    start_urls = [
        f"https://ss.ge/ka/udzravi-qoneba/l/bina/iyideba?Page={i}&RealEstateTypeId=5&RealEstateDealTypeId=4&StatusField.FieldId=34&StatusField.Type=SingleSelect&StatusField.StandardField=Status&PriceType=false&CurrencyId=1" for i in range(1,250)
    ]



    def parse(self, response):

        try:
            links = []
            for flat in response.css("div.latest_article_each "):
                id = int(flat.css('div::attr(data-id)').get())
                link = flat.css('a::attr(href)').get()

                links.append(link)


            for link in links:
                try:
                    id = int(link.split("-")[-1])
                    item = LinkItem(id = id, link = "https://ss.ge"+link)

                    pipe = FlatLinkRemodelPipeline()
                    pipe.process_item(item, self)
                except Exception as e:
                    print(e)
                    continue

        except Exception as e:
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d-%H:%M:%S")


            f = open("logs/flat_links/flat_links_logs.txt","a")
            line = "---------------------------------"
            f.write("\n" + current_time + ": " + str(e) +"\n" + line + "\n")
            f.close()
            print(e)
