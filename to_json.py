from sitkva.models import District,Subdistrict,Street
import pandas as pd

# dataframe Name and Age columns

streets = [street for street in Street.query.all()]
subdistricts = []
districts = []

for st in streets:
    sub_id = st.subdistrict_id
    sub = Subdistrict.query.filter(Subdistrict.id == sub_id).first()
    subdistricts.append(sub)


for sub in subdistricts:
    dist_id = sub.district_id
    dist = District.query.filter(District.id == dist_id).first()
    districts.append(dist)




df = pd.DataFrame({'District' : districts,
                    'Subdistrict': subdistricts,
                    'Street': streets})

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('demo.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1', index=False)

# Close the Pandas Excel writer and output the Excel file.
writer.save()
