import scrapy
from items import FlatLinkItem
from pipelines import FlatLinkPipeline
from datetime import datetime





class FlatLinksSpider(scrapy.Spider):

    name = "flat_links"

    start_urls = [
        f"https://ss.ge/ka/udzravi-qoneba/l/bina/iyideba?Page={i}&RealEstateTypeId=5&RealEstateDealTypeId=4&CurrentUserId=&Query=&MunicipalityId=&CityIdList=&subdistr=&stId=&PrcSource=&StatusField.FieldId=34&StatusField.Type=SingleSelect&StatusField.StandardField=Status&QuantityFrom=&QuantityTo=&PriceType=false&CurrencyId=1&PriceFrom=&PriceTo=&Context.Request.Query[Query]=&IndividualEntityOnly=true&Fields[3].FieldId=151&Fields[3].Type=SingleSelect&Fields[3].StandardField=None&Fields[4].FieldId=150&Fields[4].Type=SingleSelect&Fields[4].StandardField=None&Fields[5].FieldId=152&Fields[5].Type=SingleSelect&Fields[5].StandardField=None&Fields[6].FieldId=29&Fields[6].Type=SingleSelect&Fields[6].StandardField=None&Fields[7].FieldId=153&Fields[7].Type=MultiSelect&Fields[7].StandardField=None&Fields[8].FieldId=30&Fields[8].Type=SingleSelect&Fields[8].StandardField=None&Fields[0].FieldId=48&Fields[0].Type=Number&Fields[0].StandardField=None&Fields[0].ValueFrom=&Fields[0].ValueTo=&Fields[1].FieldId=146&Fields[1].Type=Number&Fields[1].StandardField=None&Fields[1].ValueFrom=&Fields[1].ValueTo=&Fields[2].FieldId=28&Fields[2].Type=Number&Fields[2].StandardField=Floor&Fields[2].ValueFrom=&Fields[2].ValueTo=&Fields[9].FieldId=14&Fields[9].Type=Group&Fields[9].StandardField=None&Fields[9].Values[0].Value=35&Fields[9].Values[0].Selected=false&Fields[9].Values[1].Value=36&Fields[9].Values[1].Selected=false&Fields[9].Values[2].Value=37&Fields[9].Values[2].Selected=false&Fields[9].Values[3].Value=38&Fields[9].Values[3].Selected=false&Fields[9].Values[4].Value=39&Fields[9].Values[4].Selected=false&Fields[9].Values[5].Value=40&Fields[9].Values[5].Selected=false&Fields[9].Values[6].Value=118&Fields[9].Values[6].Selected=false&Fields[9].Values[7].Value=120&Fields[9].Values[7].Selected=false&VipStatus=" for i in range(1,400)
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
                    item = FlatLinkItem(id = id, link = "https://ss.ge"+link)

                    pipe = FlatLinkPipeline()
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
