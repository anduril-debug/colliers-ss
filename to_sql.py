import pyodbc


server = "192.168.0.36"
username = "Valuation_User"
password = "q2b8dy8VH^W!kkU"
database = "Valuation"

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()



cursor.execute("SELECT * FROM [Valuation].[dbo].[SitkvaSakme]")
row = cursor.fetchone()
while row:
    print(row)
    row = cursor.fetchone()
