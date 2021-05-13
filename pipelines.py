from sitkva.models import FlatLink,HouseLink,Flat,House
from sitkva import db
import requests
from datetime import datetime
import sys
import sqlalchemy

now = datetime.now()
current_time = now.strftime("%Y-%m-%d-%H:%M:%S")


class FlatLinkPipeline(object):



    def process_item(self,item,spider):

        try:
            link = FlatLink( id = item["id"], link = item["link"] )
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


class HouseLinkPipeline(object):



    def process_item(self,item,spider):

        try:
            link = HouseLink( id = item["id"], link = item["link"] )
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





class FlatPipeline(object):



        def process_item(self, item, spider):

            address = item["address"]
            header = item["header"]
            outside_tbilisi = header.split()[-1][:-2]




            if address != "UNKNOWN":
                r = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyDPwqydFe-jC8JLbM0VyeQXVOBRZXo6Rak&address={address}+თბილისი")
            else:
                r = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyDPwqydFe-jC8JLbM0VyeQXVOBRZXo6Rak&address={outside_tbilisi}")


            jason = r.json()
            address_components = jason["results"][0]["address_components"]


            addresses = {
                "street_address": "",
                "route": "",
                "political": "",
                "country": "",
                "administrative_area_level_1": "",
                "administrative_area_level_2": "",
                "administrative_area_level_3": "",
                "administrative_area_level_4": "",
                "administrative_area_level_5": "",
                "locality": "",
                "sublocality": "",
                "postal_code": "",
                "natural_feature": "",
                "airport": "",
                "park": "",
                "point_of_interest": "",
            }


            latitude = jason["results"][0]["geometry"]["location"]["lat"]
            longitude = jason["results"][0]["geometry"]["location"]["lng"]

            for i in address_components:
                for j in i["types"]:
                    addresses[j] = i["long_name"]




            try:

                description = item["description"]

                if item["description"] == None:
                    description = ""



                flat = Flat(
                            id = int(item["id"]), link_id = int(item["link_id"]),header = item["header"],time = item["time"], total_area = float(item["total_area"]),
                            rooms = float(item["rooms"]),bedrooms = item["bedrooms"],stage = int(item["stage"]),total_stages = int(item["total_stages"]),
                            balcony_loggia = item["balcony_loggia"], bathtubs = item["bathtubs"],project = item["project"],state = item["state"], status = item["status"],
                            latitude = latitude,longitude =longitude,garage = item["garage"],basement = item["basement"],stockroom = item["stockroom"],
                            gas = item["gas"],central_heating = item["central_heating"],description = description,price = item["price"], currency = item["currency"],
                            price_per_m2 = item["price_per_m2"],seller = item["seller"],
                            street_address = addresses["street_address"], route = addresses["route"], political = addresses["political"], country = addresses["country"],
                            administrative_area_level_1 = addresses["administrative_area_level_1"], administrative_area_level_2 = addresses["administrative_area_level_2"],
                            administrative_area_level_3 = addresses["administrative_area_level_3"], administrative_area_level_4 = addresses["administrative_area_level_4"],
                            administrative_area_level_5 = addresses["administrative_area_level_5"], locality = addresses["locality"], sublocality = addresses["sublocality"],
                            postal_code = addresses["postal_code"], natural_feature = addresses["natural_feature"], airport = addresses["airport"], park = addresses["park"],
                            point_of_interest = addresses["point_of_interest"])


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



class HousePipeline(object):



        def process_item(self, item, spider):

            address = item["address"]
            header = item["header"]
            outside_tbilisi = header.split()[-1][:-2]




            if address != "UNKNOWN":
                r = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyDPwqydFe-jC8JLbM0VyeQXVOBRZXo6Rak&address={address}+თბილისი")
            else:
                r = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyDPwqydFe-jC8JLbM0VyeQXVOBRZXo6Rak&address={outside_tbilisi}")


            jason = r.json()
            address_components = jason["results"][0]["address_components"]


            addresses = {
                "street_address": "",
                "route": "",
                "political": "",
                "country": "",
                "administrative_area_level_1": "",
                "administrative_area_level_2": "",
                "administrative_area_level_3": "",
                "administrative_area_level_4": "",
                "administrative_area_level_5": "",
                "locality": "",
                "sublocality": "",
                "postal_code": "",
                "natural_feature": "",
                "airport": "",
                "park": "",
                "point_of_interest": "",
            }


            latitude = jason["results"][0]["geometry"]["location"]["lat"]
            longitude = jason["results"][0]["geometry"]["location"]["lng"]

            for i in address_components:
                for j in i["types"]:
                    addresses[j] = i["long_name"]




            try:




                house = House(
                            id = int(item["id"]), link_id = int(item["link_id"]),header = item["header"],time = item["time"],code = item["code"], total_area = float(item["total_area"]),
                            rooms = float(item["rooms"]), garden_area = float(item["garden_area"]),bedrooms = item["bedrooms"],state = item["state"],
                            status = item["status"],balcony_loggia = item["balcony_loggia"],garage = item["garage"], basement = item["basement"],
                            stockroom = item["stockroom"], water = item["water"], gas = item["gas"],central_heating = item["central_heating"],
                            price = item["price"], currency = item["currency"],pool = item["pool"],
                            price_per_m2 = item["price_per_m2"],seller = item["seller"],latitude = latitude, longitude = longitude,
                            street_address = addresses["street_address"], route = addresses["route"], political = addresses["political"], country = addresses["country"],
                            administrative_area_level_1 = addresses["administrative_area_level_1"], administrative_area_level_2 = addresses["administrative_area_level_2"],
                            administrative_area_level_3 = addresses["administrative_area_level_3"], administrative_area_level_4 = addresses["administrative_area_level_4"],
                            administrative_area_level_5 = addresses["administrative_area_level_5"], locality = addresses["locality"], sublocality = addresses["sublocality"],
                            postal_code = addresses["postal_code"], natural_feature = addresses["natural_feature"], airport = addresses["airport"], park = addresses["park"],
                            point_of_interest = addresses["point_of_interest"])


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
