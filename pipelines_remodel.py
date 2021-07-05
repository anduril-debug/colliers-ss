from sitkva.models import Street,Subdistrict,District,City,FlatRemodel,FlatLinkRemodel,HouseRemodel,HouseLinkRemodel
from sitkva import db
import requests
from datetime import datetime
import sys
import sqlalchemy

now = datetime.now()
current_time = now.strftime("%Y-%m-%d-%H:%M:%S")






class FlatLinkRemodelPipeline(object):



    def process_item(self,item,spider):

        try:
            link = FlatLinkRemodel( id = item["id"], link = item["link"] )
            db.session.add(link)
            db.session.commit()

            print("item id:"+str(item["id"])+" added successfuly")

            f = open(f"logs/flat_links/{current_time}-[PIPELINES]-flat_links_logs-SUCCESS.txt","a")
            line = "---------------------------------"
            f.write("\n" + current_time + ": " + "link id: " + str(item["id"]) + " successfuly added." + "\n" + line + "\n")
            f.close()




        except sqlalchemy.exc.IntegrityError:
                print("LINK ALREADY EXISTS")
                db.session.rollback()

        except Exception as e:

            f = open(f"logs/flat_links/{current_time}-[PIPELINES]-flat_links_logs.txt","a")
            line = "---------------------------------"
            f.write("\n" + current_time + ": " + str(e) +"\n" + line + "\n")
            f.close()
            print(e)

            db.session.rollback()


        return item



class HouseLinkRemodelPipeline(object):



    def process_item(self,item,spider):

        try:
            link = HouseLinkRemodel( id = item["id"], link = item["link"] )
            db.session.add(link)
            db.session.commit()

            print("item id:"+str(item["id"])+" added successfuly")

            f = open(f"logs/house_links/{current_time}-[PIPELINES]-house_links_logs-SUCCESS.txt","a")
            line = "---------------------------------"
            f.write("\n" + current_time + ": " + "link id: " + str(item["id"]) + " successfuly added." + "\n" + line + "\n")
            f.close()




        except sqlalchemy.exc.IntegrityError:
                print("LINK ALREADY EXISTS")
                db.session.rollback()

        except Exception as e:

            f = open(f"logs/house_links/{current_time}-[PIPELINES]-house_links_logs.txt","a")
            line = "---------------------------------"
            f.write("\n" + current_time + ": " + str(e) +"\n" + line + "\n")
            f.close()
            print(e)

            db.session.rollback()


        return item






class FlatRemodelPipeline(object):



        def process_item(self, item, spider):





            try:

                try:
                    address = Street.query.filter(Street.name == item["address"]).first()
                    subdistrict = address.subdistrict
                    district = subdistrict.district
                    city = district.city
                except:
                    address = Street.query.filter(Street.id == 9999).first()
                    subdistrict = address.subdistrict
                    district = subdistrict.district
                    city = district.city



                flat = FlatRemodel(
                            id = int(item["id"]), link_id = int(item["link_id"]),header = item["header"],time = item["time"], total_area = float(item["total_area"]),
                            rooms = float(item["rooms"]),bedrooms = item["bedrooms"],stage = int(item["stage"]),total_stages = int(item["total_stages"]),
                            balcony_loggia = item["balcony_loggia"], bathtubs = item["bathtubs"],project = item["project"],state = item["state"], status = item["status"],
                            garage = item["garage"],basement = item["basement"],stockroom = item["stockroom"],
                            gas = item["gas"],central_heating = item["central_heating"],price = item["price"], currency = item["currency"],
                            price_per_m2 = item["price_per_m2"],seller = item["seller"],
                            administrative_area_level_1 = item["administrative_area_level_1"],
                            administrative_area_level_2 = item["administrative_area_level_2"],
                            administrative_area_level_3 = item["administrative_area_level_3"],
                            administrative_area_level_4 = item["administrative_area_level_4"],
                            address = address.name, subdistrict = subdistrict.name, district = district.name, city = city.name, is_used = "no"
                            )

                db.session.add(flat)
                db.session.commit()
                print("flad id: "+str(item["id"])+" successfuly added")

                f = open(f"logs/flats/{current_time}-[PIPELINES]-flat_logs-SUCCESS.txt","a")
                line = "---------------------------------"
                f.write("\n" + current_time + ": " + "flat id:" + str(item["id"]) + " added" + "\n" + "link id: " + str(item["link_id"]) + "\n" + line + "\n")
                f.close()





            except sqlalchemy.exc.IntegrityError:
                print("INTEGITY ERROR")
                db.session.rollback()


            except Exception as e:


                f = open(f"logs/flats/{current_time}-[PIPELINES]-flat_logs.txt-FAILURE","a")
                line = "---------------------------------"
                f.write("\n" + current_time + ": " + str(e) + "\n" + line + "\n")
                f.close()

                db.session.rollback()
                print(e)





            return item








class HouseRemodelPipeline(object):



        def process_item(self, item, spider):



            try:

                try:
                    address = Street.query.filter(Street.name == item["address"]).first()
                    subdistrict = address.subdistrict
                    district = subdistrict.district
                    city = district.city
                except:
                    address = Street.query.filter(Street.id == 9999).first()
                    subdistrict = address.subdistrict
                    district = subdistrict.district
                    city = district.city


                house = HouseRemodel(
                            id = int(item["id"]), link_id = int(item["link_id"]),header = item["header"],time = item["time"],code = item["code"], total_area = float(item["total_area"]),
                            rooms = float(item["rooms"]), garden_area = float(item["garden_area"]),bedrooms = item["bedrooms"],state = item["state"],
                            status = item["status"],balcony_loggia = item["balcony_loggia"],garage = item["garage"], basement = item["basement"],
                            stockroom = item["stockroom"], water = item["water"], gas = item["gas"],central_heating = item["central_heating"],
                            price = item["price"], currency = item["currency"],pool = item["pool"],
                            price_per_m2 = item["price_per_m2"],seller = item["seller"],
                            administrative_area_level_1 = item["administrative_area_level_1"],
                            administrative_area_level_2 = item["administrative_area_level_2"],
                            administrative_area_level_3 = item["administrative_area_level_3"],
                            administrative_area_level_4 = item["administrative_area_level_4"],
                            address = address.name, subdistrict = subdistrict.name, district = district.name, city = city.name, is_used = "no")

                db.session.add(house)
                db.session.commit()
                print("house id: "+str(item["id"])+" successfuly added")

                f = open(f"logs/houses/{current_time}-[PIPELINES]-house_logs-SUCCESS.txt","a")
                line = "---------------------------------"
                f.write("\n" + current_time + ": " + "house id:" + str(item["id"]) + " added" + "\n" + "link id: " + str(item["link_id"]) + "\n" + line + "\n")
                f.close()





            except Exception as e:

                f = open(f"logs/houses/{current_time}-[PIPELINES]-house_logs.txt-FAILURE","a")
                line = "---------------------------------"
                f.write("\n" + current_time + ": " + str(e) + "\n" + line + "\n")
                f.close()

                db.session.rollback()
                print(e)





            return item
