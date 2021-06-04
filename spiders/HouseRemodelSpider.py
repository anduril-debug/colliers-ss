import scrapy
from items import HouseItem
from sitkva import db
from sitkva.models import HouseLinkRemodel
from pipelines_remodel import HouseRemodelPipeline
from datetime import datetime


now = datetime.now()
running_time = now.strftime("%Y-%m-%d-%H:%M:%S")






class HouseSpider(scrapy.Spider):

    name = "house"

    urls = [link.link for link in HouseLinkRemodel.query.filter(HouseLinkRemodel.house == None).all()]


    start_urls = urls



    def parse(self, response):

        try:
            header = response.css("div.article_in_title > h1::text").get()
            time = response.css("div.add_date_block::text").get()
            time = time.split('/')[0].strip()

            address_div = response.css('div.StreeTaddressList')

            if address_div != []:
                full_address = address_div.css('a::text').get()
                full_address = " ".join(full_address.split())
                address = " ".join(full_address.split()[:-1])
            else:
                full_address = "UNKNOW"
                address = "UNKNOW"




            main_details = {
                "სახლის ფართი" : "-1",
                "ოთახები" : "-1",
                "საძინებლები" : "-1",
            }


            main_dets = response.css('div.EAchParamsBlocks')

            for d in main_dets:

                title = d.css("div.ParamsBotBlk::text").get().strip()
                if title == "სახლის ფართი":
                    desc = d.css("text::text").get().strip()
                    desc = float(desc.split("m")[0])
                else:
                    desc = float(d.css("text::text").get().strip())
                main_details[title] = desc



            details = {
                "ეზოს ფართი" : "-1",
                "მდგომარეობა" : "NO_INFO",
                "სტატუსი" : "NO_INFO"
            }


            dets = response.css('div.ProjBotEach')

            for d in dets:
                title = d.css("span.TitleEachparbt::text").get()
                title = title.replace(":","").strip()

                if title == "სტატუსი":
                    desc = d.css("text::text").get()
                else:
                    desc = d.css("span.PRojeachBlack::text").get()
                    desc = desc.strip()

                details[title] = desc


            additional_info = {
                "აუზით" : "NO",
                "გარაჟი" : "NO",
                "აივანი" : "NO",
                "სარდაფი" : "NO",
                "სათავსო" : "NO",
                "ბუნებრივი აირი" : "NO",
                "სასმელი წყლით" : "NO",
                "ცენტრალური გათბობა" : "NO"
            }

            dets = response.xpath(".//div[contains(@class, 'parameteres_item_each') and not(contains(@class, 'lacking'))]//text()")

            for d in dets:
                additional_info[d.get().strip()] = "YES"




            price_div = response.css("div.desktopPriceBlockDet")
            price = price_div.css("div.price::text").get().strip()
            try:
                price = float(price.replace(" ",""))
            except:
                price = "შეთანხმებით"


            try:
                currency = response.xpath(".//span[contains(@class, 'curr_item') and not(contains(@style, 'display:none'))]//text()").get()
            except:
                currency = ""

            unit_price_div = response.css("div.item_unit_price")
            try:
                unit_price = unit_price_div.css("span.price_item::text").get()
                unit_price = float(unit_price.strip().replace(" ",''))
            except:
                unit_price = "შეთანხმებით"

            seller_div = response.css("div.author_type")

            seller_text = seller_div.css('a::text').get().strip()

            if seller_text == "ყველა განცხადება":
                seller = "ფიზიკური პირი"
            elif seller_text == "სააგენტოს ყველა განცხადება":
                seller = "სააგენტო"
            elif seller_text == "აგენტის ყველა განცხადება":
                seller = "აგენტი"
            elif seller_text == "კომპანიის ყველა განცხადება":
                seller = "სამშენებლო კომპანია"
            else:
                seller = "UKNOWN"




            code = response.css("div.code::text").get()
            if code:
                code = code.split(":")[-1]
            else:
                code = "UNKNOWN"




            id = response.css("#main-body > div.all_page_blocks > div.container.realestateDtlSlider > div.col-md-9.col-xs-9.DetailedMd9 > div.detailed_article_body > div.DetailedPageAllBodyBLock > div.DetailedLeftAll > div.article_head_block.flex-center > div.LeftHeadBlock.veri-block > div > span::text").get()




            house = HouseItem(  id = int(id), link_id = int(id),
                                header = header,address = full_address,time = time, code = code,
                                total_area = main_details["სახლის ფართი"], rooms = main_details["ოთახები"],garden_area = details["ეზოს ფართი"].split("m")[0], bedrooms = main_details["საძინებლები"],
                                state = details["მდგომარეობა"], status = details["სტატუსი"],pool = additional_info["აუზით"],
                                balcony_loggia = additional_info["აივანი"],
                                garage = additional_info["გარაჟი"], basement = additional_info["სარდაფი"], stockroom = additional_info["სათავსო"],water = additional_info["სასმელი წყლით"],
                                gas = additional_info["ბუნებრივი აირი"], central_heating = additional_info["ცენტრალური გათბობა"],
                                price = price, currency = currency, price_per_m2 = unit_price, seller = seller)

            pipe = HouseRemodelPipeline()
            pipe.process_item(house,self)




        except Exception as e:
                link_id = response.url.split("-")[-1]


                if str(e) == "int() argument must be a string, a bytes-like object or a number, not 'NoneType'" or str(e) == "'NoneType' object has no attribute 'split'":
                    house_link = HouseLinkRemodel.query.filter_by(id = int(link_id)).first()
                    db.session.delete(house_link)
                    db.session.commit()
                    print("Link has been removed")


                now = datetime.now()
                current_time = now.strftime("%Y-%m-%d-%H:%M:%S")

                f = open(f"logs/houses/-{running_time}-[SPIDER]-house_logs.txt","a")
                line = "---------------------------------"
                f.write("\n" + current_time + " : " + str(e) + "\n\n" + str(response.url) + "\n" + line + "\n")
                f.close()
                print(e)
