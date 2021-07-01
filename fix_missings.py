from sitkva import db
from sitkva.models import FlatRemodel,HouseRemodel


def fix_missing_flats():

    filleds = FlatRemodel.query.filter(FlatRemodel.rooms > 0).all()
    total_areas = 0
    total_rooms = 0

    for f in filleds:
        total_areas += f.total_area
        total_rooms += f.rooms

    avg = int(total_areas/total_rooms)

    misseds = FlatRemodel.query.filter(FlatRemodel.rooms <= 0).all()
    for f in misseds:
        print(f"rooms {f.rooms} changed to {int(f.total_area/avg)}, total area = {f.total_area}")
        f.rooms = int(f.total_area/avg)
        db.session.add(f)
        db.session.commit()



def fix_missing_houses():
    filleds = HouseRemodel.query.filter(HouseRemodel.rooms > 0).all()
    total_areas = 0
    total_rooms = 0

    for f in filleds:
        total_areas += f.total_area
        total_rooms += f.rooms

    avg = int(total_areas/total_rooms)

    misseds = HouseRemodel.query.filter(HouseRemodel.rooms <= 0).all()
    for f in misseds:
        print(f"rooms {f.rooms} changed to {int(f.total_area/avg)}, total area = {f.total_area}")
        f.rooms = int(f.total_area/avg)
        db.session.add(f)
        db.session.commit()
