from sitkva.models import *
from sitkva import db


subdistricts = ["აბანოთუბანი","ავლაბარი","ელია","ვერა","მთაწმინდა","სოლოლაკი"]




j = 1

for i in subdistricts:
    sd = Subdistrict(id = 500+j, name = i,district_id = 105)
    j += 1
    db.session.add(sd)
    db.session.commit()
