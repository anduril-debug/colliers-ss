import scrapy
from items import FlatItem
from sitkva import db
from sitkva.models import FlatLink
from pipelines import FlatPipeline
from datetime import datetime


now = datetime.now()
running_time = now.strftime("%Y-%m-%d-%H:%M:%S")




class FlatSpider(scrapy.Spider):

    name = "flat"

    start_urls = [link.link for link in FlatLink.query.filter(FlatLink.flat == None).all()]



    def parse(self, response):

        try:
            id_div = response.css('div.article_item_id')
            id = int(id_div.css('span::text').get())

            link = FlatLink.query.filter_by(id = id).first()
            link_id = link.id


            header = response.css("div.article_in_title > h1::text").get()

            time_div = response.css('div.add_date_block::text').get()
            time = time_div.split('/')[0].strip()

            address_div = response.css('div.StreeTaddressList')

            if address_div != []:
                full_address = address_div.css('a::text').get()
                full_address = " ".join(full_address.split())
                address = " ".join(full_address.split()[:-1])
                city = "თბილისი"
            else:
                full_address = "UNKNOW"
                address = "UNKNOW"
                city_div = response.css("div.article_in_title")
                city = city_div.css('h1::text').get().split()[-1]



            main_details = {
                "საერთო ფართი" : "NO_INFO",
                "ოთახები" : "NO_INFO",
                "საძინებლები" : "NO_INFO",
                "სართული" : "NO_INFO",
            }


            main_dets = response.css('div.EAchParamsBlocks')

            for d in main_dets:

                title = d.css("div.ParamsBotBlk::text").get().strip()
                if title == "საერთო ფართი":
                    desc = d.css("text::text").get().strip()
                    desc = float(desc.split("m")[0])
                else:
                    desc = d.css("text::text").get().strip()





                main_details[title] = desc



            total_stages = response.css("span.all-floors::text").get()
            total_stages = total_stages.strip()[1:]

            details = {
                "აივანი/ლოჯია" : "NO_INFO",
                "სველი წერტილი" : "NO_INFO",
                "პროექტი" : "NO_INFO",
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
                "ცენტრალური გათბობა" : "NO",
                "ბუნებრივი აირი" : "NO",
                "სათავსო" : "NO",
                "სარდაფი" : "NO",
                "აივანი" : "NO",
                "გარაჟი" : "NO",
                "ბოლო სართული" : "NO",
                "ლიფტი" : "NO"
            }

            dets = response.xpath(".//div[contains(@class, 'parameteres_item_each') and not(contains(@class, 'lacking'))]//text()")

            for d in dets:
                additional_info[d.get().strip()] = "YES"


            desc_div = response.css("div.article_item_desc_body")
            description = desc_div.css("span.details_text::text").get()


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




            #თუ უკავია რამოდენიმე სართული
            stage = main_details["სართული"]
            stage = stage.split(",")
            multi_stages = []

            for s in stage:
                s_list = s.split("-")
                if len(s_list) == 2:
                    for i in range(int(s_list[0]),int(s_list[1])+1):
                        multi_stages.append(i)
                else:
                    multi_stages.append(int(s_list[0]))




            for stage in multi_stages:

                #id by stage
                uid = str(id)
                uid += str(stage)


                flat = FlatItem(id = int(uid),link_id = id, link = response.request.url, header = header, city = city, address = full_address,time = time,
                            total_area = main_details["საერთო ფართი"], rooms = float(main_details["ოთახები"]), bedrooms = float(main_details["საძინებლები"]),
                            stage = stage, total_stages = total_stages, balcony_loggia = details["აივანი/ლოჯია"],
                            bathtubs = details["სველი წერტილი"], project = details["პროექტი"], state = details["მდგომარეობა"], status = details["სტატუსი"],
                            garage = additional_info["გარაჟი"], basement = additional_info["სარდაფი"], stockroom = additional_info["სათავსო"],
                            gas = additional_info["ბუნებრივი აირი"], elevator = additional_info["ლიფტი"], central_heating = additional_info["ცენტრალური გათბობა"],
                            description = description, price = price, currency = currency, price_per_m2 = unit_price, seller = seller)

                pipe = FlatPipeline()
                pipe.process_item(flat,self)



        except Exception as e:
                link_id = response.url.split("-")[-1]


                if str(e) == "int() argument must be a string, a bytes-like object or a number, not 'NoneType'":
                    flat_link = FlatLink.query.filter_by(id = int(link_id)).first()
                    db.session.delete(flat_link)
                    db.session.commit()
                    print("Link has been removed")


                now = datetime.now()
                current_time = now.strftime("%Y-%m-%d-%H:%M:%S")

                f = open(f"logs/flats/-{running_time}-[SPIDER]-flat_logs.txt","a")
                line = "---------------------------------"
                f.write("\n" + current_time + " : " + str(e) + "\n\n" + str(response.url) + "\n" + line + "\n")
                f.close()
                print(e)
