import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()
SERVER = os.environ.get("COLLIERS_SQL_ADDRESS")
USERNAME = os.environ.get("COLLIERS_USER")
PASSWORD = os.environ.get("COLLIERS_USER_PASSWORD")
DATABASE = os.environ.get("COLLIERS_DATABASE")

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+SERVER+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD)
cursor = cnxn.cursor()



cursor.execute("SELECT * FROM [Valuation].[dbo].[SitkvaSakme]")
row = cursor.fetchone()
while row:
    print(row)
    row = cursor.fetchone()
