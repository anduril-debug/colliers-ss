from bs4 import BeautifulSoup
import requests
from psycopg2 import connect, sql
import os
import pyodbc
import datetime
import json
from sitkva import db
from sitkva.models import FlatRemodel,HouseRemodel


now = datetime.datetime.now()
current_time = now.strftime("%Y-%m-%d-%H:%M")


## modeling and projects standarts

modeling = {
    "მწვანე კარკასი" : "თეთრი კარკასი",
    "თეთრი კარკასი" : "თეთრი კარკასი",
    "თბილი კარკასი" : "თეთრი კარკასი",
    "პრემიუმ კარკასი" : "თეთრი კარკასი",
    "ძველი რემონტით" : "ძველი რემონტი",
    "ძველი რემონტი" : "ძველი რემონტი",
    "ახალი რემონტი" : "ახალი რემონტი",
    "ახალი რემონტით" : "ახალი რემონტი",
    "გარემონტებული" : "ახალი რემონტი",
    "შავი კარკასი" : "შავი კარკასი",
    "მიმდინარე რემონტი" : "მიმდინარე რემონტით",
    "მიმდინარე რემონტი" : "მიმდინარე რემონტი",
    "სარემონტო" : "სარემონტო",
    "NO_INFO" : "უცნობი"
}


projects = {
    "არასტანდარტული" : "არასტანდარტული",
    "ქალაქური" : "ქალაქური",
    "ლვოვის" : "ლვოვი",
    "ლვოვი" : "ლვოვი",
    "NO_INFO" : "უცნობი",
    "ჩეხური" : "ჩეხური",
    "დუპლექსი" : "დუპლექსი",
    "ვეძისი" : "ვეძისი",
    "ვეძისის" : "ვეძისი",
    "ყავლაშვილის" : "ყავლაშვილი",
    "ყავლაშვილი" : "ყავლაშვილი",
    "ხრუშჩოვის" : "ხრუშჩოვი",
    "ხრუშჩოვი" : "ხრუშჩოვი",
    "მეტრომშენი" : "მეტრომშენი",
    "მეტრომშენის" : "მეტრომშენი",
    "თბილისური ეზო" : "თბილისური ეზო",
    "მოსკოვის" : "მოსკოვი",
    "მოსკოვი" : "მოსკოვი",
    "თუხარელის" : "თუხარელი",
    "თუხარელი" : "თუხარელის",
    "იუგოსლავიის" : "იუგოსლავია",
    "იუგოსლავია" : "იუგოსლავია",
    "კიევის" : "კიევი",
    "კიევი" : "კიევი",
    "ლენინგრადის" : "ლენინგრადი",
    "ლენინგრადი" : "ლენინგრადი"
}


projects_types = {
    'ძველი აშენებული' : 'Old',
    'ახალი აშენებული' : 'New',
    'მშენებარე' : 'Under Construction',
    'NO_INFO' : 'უცნობი'
}

# Uploading into MS SQL

# flats = FlatRemodel.query.filter(FlatRemodel.price != "შეთანხმებით").all()

### read Colliers Subdistricts json

coll_subs_json = open('colliers_subs.json')

coll_subs = json.load(coll_subs_json)

coll_subs_json.close()









def usd_to_gel():
    r = requests.get("https://www.nbg.gov.ge/index.php?m=582&lng=geo")
    soup = BeautifulSoup(r.content, 'html.parser')


    table = soup.find('div',id="currency_id")

    table_rows = table.find_all('tr')

    usd = table_rows[-3]

    tds = usd.find_all('td')

    currency = None


    if tds[0].text.strip() == "USD":
        currency = tds[2].text.strip()

    return float(currency)
LARIS_KURSI = usd_to_gel()



def connect_to_colliers_db():
    SERVER = os.environ.get("COLLIERS_SQL_ADDRESS")
    USERNAME = os.environ.get("COLLIERS_USER")
    PASSWORD = os.environ.get("COLLIERS_USER_PASSWORD")
    DATABASE = os.environ.get("COLLIERS_DATABASE")

    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+SERVER+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD)

    return cnxn



def connect_to_local_db():
    conn = connect(
        dbname = os.environ["LOCAL_SERVER_DB"],
        user = os.environ["LOCAL_DB_USERNAME"],
        host = os.environ["LOCAL_SERVER_HOST"],
        password = os.environ["LOCAL_DB_PASSWORD"]
    )

    return conn


def create_local_tmp_flats(cursor,conn):
    cursor.execute("""
                    SELECT flat_remodel.id,flat_remodel.time,flat_remodel.total_area,flat_remodel.rooms,flat_remodel.stage,flat_remodel.total_stages,
                    		flat_remodel.administrative_area_level_1,flat_remodel.district,
                    		flat_remodel.subdistrict,flat_remodel.address,flat_remodel.project,flat_remodel.state,flat_remodel.status,
                            administrative_area.latitude,administrative_area.longitude,flat_remodel.price,flat_remodel.price_per_m2,flat_remodel.currency
                    		INTO flat_tmp_colliers_outside_tbilisi
                    FROM flat_remodel
                    LEFT JOIN administrative_area ON flat_remodel.administrative_area_level_1 = administrative_area.name
                    WHERE flat_remodel.administrative_area_level_1 != 'თბილისი' AND flat_remodel.is_used = 'no';

                    ALTER TABLE flat_tmp_colliers_outside_tbilisi
                    ADD COLUMN property varchar(255) DEFAULT 'ბინა',
                    ADD COLUMN sale_status varchar(255) DEFAULT 'Sale',
                    ADD COLUMN sector varchar(255) DEFAULT '',
                    ADD COLUMN region varchar(255) DEFAULT '',
                    ADD COLUMN full_cadastral_code varchar(255) DEFAULT '',
                    ADD COLUMN land_cadastral_code varchar(255) DEFAULT '',
                    ADD COLUMN pipeline_project varchar(255) DEFAULT '',
                    ADD COLUMN pipeline_subproject varchar(255) DEFAULT '',
                    ADD COLUMN parent_developer varchar(255) DEFAULT '',
                    ADD COLUMN completion_period varchar(255) DEFAULT '',
                    ADD COLUMN is_mp_overall varchar(255) DEFAULT '';


                """)

    cursor.execute("""
                    SELECT flat_remodel.id,flat_remodel.time,flat_remodel.total_area,flat_remodel.rooms,flat_remodel.stage,flat_remodel.total_stages,
                    		flat_remodel.administrative_area_level_1,flat_remodel.district,
                    		flat_remodel.subdistrict,flat_remodel.address,flat_remodel.project,flat_remodel.state,flat_remodel.status,street.latitude,street.longitude,
                            flat_remodel.price,flat_remodel.price_per_m2,flat_remodel.currency
                    		INTO flat_tmp_colliers_tbilisi
                    FROM flat_remodel
                    LEFT JOIN street ON flat_remodel.address=street.name
                    WHERE flat_remodel.administrative_area_level_1 = 'თბილისი' AND flat_remodel.is_used = 'no' ;


                    ALTER TABLE flat_tmp_colliers_tbilisi
                    ADD COLUMN property varchar(255) DEFAULT 'ბინა',
                    ADD COLUMN sale_status varchar(255) DEFAULT 'Sale',
                    ADD COLUMN sector varchar(255) DEFAULT '',
                    ADD COLUMN region varchar(255) DEFAULT '',
                    ADD COLUMN full_cadastral_code varchar(255) DEFAULT '',
                    ADD COLUMN land_cadastral_code varchar(255) DEFAULT '',
                    ADD COLUMN pipeline_project varchar(255) DEFAULT '',
                    ADD COLUMN pipeline_subproject varchar(255) DEFAULT '',
                    ADD COLUMN parent_developer varchar(255) DEFAULT '',
                    ADD COLUMN completion_period varchar(255) DEFAULT '',
                    ADD COLUMN is_mp_overall varchar(255) DEFAULT '';


                """)
    conn.commit()
    print("tmp flats has been created...")


def create_local_tmp_houses(cursor,conn):
    cursor.execute("""
                    SELECT house_remodel.id,house_remodel.time,house_remodel.total_area,house_remodel.garden_area,house_remodel.rooms,
                    		house_remodel.administrative_area_level_1,house_remodel.district,
                    		house_remodel.subdistrict,house_remodel.address,house_remodel.state,house_remodel.status,
                            administrative_area.latitude,administrative_area.longitude,house_remodel.price,house_remodel.price_per_m2,house_remodel.currency
                    		INTO house_tmp_colliers_outside_tbilisi
                    FROM house_remodel
                    LEFT JOIN administrative_area ON house_remodel.administrative_area_level_1 = administrative_area.name
                    WHERE house_remodel.administrative_area_level_1 != 'თბილისი' AND house_remodel.is_used = 'no';

                    ALTER TABLE house_tmp_colliers_outside_tbilisi
                    ADD COLUMN property varchar(255) DEFAULT 'სახლი',
                    ADD COLUMN sale_status varchar(255) DEFAULT 'Sale',
                    ADD COLUMN sector varchar(255) DEFAULT '',
                    ADD COLUMN region varchar(255) DEFAULT '',
                    ADD COLUMN full_cadastral_code varchar(255) DEFAULT '',
                    ADD COLUMN land_cadastral_code varchar(255) DEFAULT '',
                    ADD COLUMN pipeline_project varchar(255) DEFAULT '',
                    ADD COLUMN pipeline_subproject varchar(255) DEFAULT '',
                    ADD COLUMN parent_developer varchar(255) DEFAULT '',
                    ADD COLUMN completion_period varchar(255) DEFAULT '',
                    ADD COLUMN is_mp_overall varchar(255) DEFAULT '';


                """)

    cursor.execute("""
                    SELECT house_remodel.id,house_remodel.time,house_remodel.total_area,house_remodel.garden_area,house_remodel.rooms,
                    		house_remodel.administrative_area_level_1,house_remodel.district,
                    		house_remodel.subdistrict,house_remodel.address,house_remodel.state,house_remodel.status,street.latitude,street.longitude,
                            house_remodel.price,house_remodel.price_per_m2,house_remodel.currency
                    		INTO house_tmp_colliers_tbilisi
                    FROM house_remodel
                    LEFT JOIN street ON house_remodel.address=street.name
                    WHERE house_remodel.administrative_area_level_1 = 'თბილისი' AND house_remodel.is_used = 'no';


                    ALTER TABLE house_tmp_colliers_tbilisi
                    ADD COLUMN property varchar(255) DEFAULT 'სახლი',
                    ADD COLUMN sale_status varchar(255) DEFAULT 'Sale',
                    ADD COLUMN sector varchar(255) DEFAULT '',
                    ADD COLUMN region varchar(255) DEFAULT '',
                    ADD COLUMN full_cadastral_code varchar(255) DEFAULT '',
                    ADD COLUMN land_cadastral_code varchar(255) DEFAULT '',
                    ADD COLUMN pipeline_project varchar(255) DEFAULT '',
                    ADD COLUMN pipeline_subproject varchar(255) DEFAULT '',
                    ADD COLUMN parent_developer varchar(255) DEFAULT '',
                    ADD COLUMN completion_period varchar(255) DEFAULT '',
                    ADD COLUMN is_mp_overall varchar(255) DEFAULT '';
                """)

    conn.commit()
    print("tmp houses has been created...")




def insert_into_ms_sql_flats(items,colliers_cursor):
    for i in items:
        try:

            flat = FlatRemodel.query.filter(FlatRemodel.id == i[0]).first()

            #converting time from dd.mm.YYYY to YYYY-mm-dd
            time = i[1].strip()
            time = datetime.datetime.strptime(time,"%d.%m.%Y").strftime("%Y-%m-%d")
            price = float(i[15])
            price_per_m2 = i[16]
            currency = i[17].strip()

            #converting price
            if currency == "U":
                price = int(price/LARIS_KURSI)
                price_per_m2 = int(price/i[2])
                currency = "$"


            remodeling = i[11].split(',')
            if len(remodeling) > 1:
                continue

            sql_inser = "INSERT INTO ss_flats VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            colliers_cursor.execute(sql_inser,i[0],time or None,i[2] or None,i[3] or None,i[4] or None,i[5] or None,i[6] or None,i[7] or None,
                                    i[8] or None,i[9] or None,projects[i[10].strip()] or None,modeling[remodeling[0].strip()] or None,projects_types[i[12].strip()] or None,i[13] or None,
                                    i[14] or None,price or None,price_per_m2 or None,currency or None,i[18] or None,i[19] or None,i[20] or None,i[21] or None,
                                    i[22] or None,i[23] or None,i[24] or None,i[25] or None,i[26] or None,i[27] or None,i[28] or None)

            colliers_cursor.commit()

            flat.is_used = "yes"
            db.session.add(flat)
            db.session.commit()


            print(f"{i[18]} has been added -- {i[6]}")
        except Exception as e:
            print("error",e)
            f = open(f"logs/colliers/{current_time}-[insert_into_ms_sql_flats].txt","a")
            line = "---------------------------------"
            f.write("\n" + str(e) + "\n")
            f.close()
            continue






def insert_into_ms_sql_houses(items, colliers_cursor):
    for i in items:
        try:
            house = HouseRemodel.query.filter(HouseRemodel.id == i[0]).first()
            #converting time from dd.mm.YYYY to YYYY-mm-dd
            time = i[1].strip()
            time = datetime.datetime.strptime(time,"%d.%m.%Y").strftime("%Y-%m-%d")
            price = float(i[13])
            price_per_m2 = i[14]
            currency = i[15].strip()

            #converting price
            if currency == "U":
                price = int(price/LARIS_KURSI)
                price_per_m2 = int(price/i[2])
                currency = "$"



            remodeling = i[9].split(',')
            if len(remodeling) > 1:
                continue

            sql_inser = "INSERT INTO ss_houses VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            colliers_cursor.execute(sql_inser,i[0],time or None,i[2] or None,i[3] or None,i[4] or None,
                                    i[5] or None,i[6] or None,i[7] or None,
                                    i[8]or None,modeling[remodeling[0].strip()] or None,projects_types[i[10].strip()] or None,i[11] or None,
                                    i[12] or None,price or None,price_per_m2 or None,currency or None,i[16] or None,i[17] or None,i[18] or None,i[19] or None,
                                    i[20] or None,i[21] or None,i[22]or None,i[23]or None,i[24]or None,i[25]or None,
                                    i[26] or None)

            colliers_cursor.commit()

            house.is_used = "yes"
            db.session.add(house)
            db.session.commit()


            print(f"{i[16]} has been added -- {i[5]}")
        except Exception as e:
            print("error",e)
            f = open(f"logs/colliers/{current_time}-[insert_into_ms_sql_houses].txt","a")
            line = "---------------------------------"
            f.write("\n" + str(e) + "\n")
            f.close()
            continue













def drop_local_tmps(cursor,conn):
    try:
        cursor.execute("""
                        DROP TABLE flat_tmp_colliers_outside_tbilisi;
                        DROP TABLE flat_tmp_colliers_tbilisi;
                        DROP TABLE house_tmp_colliers_outside_tbilisi;
                        DROP TABLE house_tmp_colliers_tbilisi;
                    """)
        conn.commit()
        print("local tmp tables has been removed...")
    except Exception as e:
        print(e)
