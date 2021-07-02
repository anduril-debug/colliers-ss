import pyodbc
import os
from dotenv import load_dotenv

from sitkva.models import FlatRemodel

import json

import datetime

from to_sql_additionals import usd_to_gel,connect_to_colliers_db,connect_to_local_db,create_local_tmp_flats,drop_local_tmp_flats,drop_local_tmp_houses,insert_into_ms_sql_flats,insert_into_ms_sql_houses,create_local_tmp_houses




load_dotenv()
cnxn = connect_to_colliers_db()
colliers_cursor = cnxn.cursor()




#### temporary sql tables

import sys


###local db connect
try:
    conn = connect_to_local_db()
    cursor = conn.cursor()
    print("CONNECTED TO LOCAL DB")

except Exception as e:
    cursor = None
    print("can't connect to DB")
    raise e




try:
    # drop_local_tmp_flats(cursor,conn)
    # drop_local_tmp_houses(cursor,conn)


    print("Creating tmps...")
    create_local_tmp_flats(cursor,conn)
    create_local_tmp_houses(cursor,conn)

    print("ADDED TMPs TO DB SUCCESSFULLY")

except Exception as e:
    print(e)
    conn.rollback()





cursor.execute("SELECT * FROM flat_tmp_colliers_outside_tbilisi WHERE price != 'შეთანხმებით'")
flats_outside_tbilisi = cursor.fetchall()

cursor.execute("SELECT * FROM house_tmp_colliers_outside_tbilisi WHERE price != 'შეთანხმებით' ")
houses_outside_tbilisi = cursor.fetchall()

cursor.execute("SELECT * FROM flat_tmp_colliers_tbilisi WHERE price != 'შეთანხმებით'")
flats_tbilisi = cursor.fetchall()

cursor.execute("SELECT * FROM house_tmp_colliers_tbilisi WHERE price != 'შეთანხმებით'")
houses_tbilisi = cursor.fetchall()



try:
    print("Start inserting....")
    insert_into_ms_sql_houses(houses_tbilisi,colliers_cursor)
    insert_into_ms_sql_houses(houses_outside_tbilisi,colliers_cursor)
    insert_into_ms_sql_flats(flats_outside_tbilisi,colliers_cursor)
    insert_into_ms_sql_flats(flats_tbilisi,colliers_cursor)

except Exception as e:
    print(e)
    drop_local_tmp_flats(cursor,conn)
    drop_local_tmp_houses(cursor,conn)
    raise e



###delete tmp tables
drop_local_tmp_flats(cursor,conn)
drop_local_tmp_houses(cursor,conn)
print("tmp tables has been removed!")
colliers_cursor.commit()
colliers_cursor.close()
cursor.close()
conn.close()
