from sitkva import db



class FlatLink(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    link = db.Column(db.String)
    flat = db.relationship('Flat', uselist=False, backref = 'flat_link',cascade="all, delete")
    def __repr__(self):
        return f"id: {self.id}"



class Flat(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    link_id = db.Column(db.Integer, db.ForeignKey('flat_link.id',ondelete="CASCADE"))
    header = db.Column(db.String(256))
    time = db.Column(db.String(16))

    #main details
    total_area = db.Column(db.Float)
    rooms = db.Column(db.Float)
    bedrooms = db.Column(db.String(128))
    stage = db.Column(db.Integer)
    total_stages = db.Column(db.Integer)


    #addresses
    street_address = db.Column(db.String(256))
    route = db.Column(db.String(256))
    political = db.Column(db.String(256))
    country = db.Column(db.String(256))
    administrative_area_level_1 = db.Column(db.String(256))
    administrative_area_level_2 = db.Column(db.String(256))
    administrative_area_level_3 = db.Column(db.String(256))
    administrative_area_level_4 = db.Column(db.String(256))
    administrative_area_level_5 = db.Column(db.String(256))
    locality = db.Column(db.String(256))
    sublocality = db.Column(db.String(256))
    postal_code = db.Column(db.String(256))
    natural_feature = db.Column(db.String(256))
    airport = db.Column(db.String(256))
    park = db.Column(db.String(256))
    point_of_interest = db.Column(db.String(256))




    #all details
    balcony_loggia = db.Column(db.String(128))
    bathtubs = db.Column(db.String(128))
    project = db.Column(db.String(128))
    state = db.Column(db.String(32))
    status = db.Column(db.String(128))

    #address

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    #additional information

    garage = db.Column(db.String(64))
    basement = db.Column(db.String(64))
    stockroom = db.Column(db.String(64))
    gas = db.Column(db.String(64))
    central_heating = db.Column(db.String(64))

    description = db.Column(db.String(5000))

    #price and seller
    price = db.Column(db.String(32))
    currency = db.Column(db.String(64))
    price_per_m2 = db.Column(db.String(32))
    seller = db.Column(db.String(64))


    #ფიზიკური პირი, უძრავი ქონების აგენტი, უძრავი ქონების სააგენტო, სამშენებლო კომპანია


    def __repr__(self):
        return f"{self.id}"





class HouseLink(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    link = db.Column(db.String)
    house = db.relationship('House', uselist=False, backref = 'house_link',cascade="all, delete")


    def __repr__(self):
        return f"id: {self.id}"



class House(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    link_id = db.Column(db.Integer, db.ForeignKey('house_link.id',ondelete="CASCADE"))

    code = db.Column(db.String(256))
    time = db.Column(db.String(16))


    #addresses
    street_address = db.Column(db.String(256))
    route = db.Column(db.String(256))
    political = db.Column(db.String(256))
    country = db.Column(db.String(256))
    administrative_area_level_1 = db.Column(db.String(256))
    administrative_area_level_2 = db.Column(db.String(256))
    administrative_area_level_3 = db.Column(db.String(256))
    administrative_area_level_4 = db.Column(db.String(256))
    administrative_area_level_5 = db.Column(db.String(256))
    locality = db.Column(db.String(256))
    sublocality = db.Column(db.String(256))
    postal_code = db.Column(db.String(256))
    natural_feature = db.Column(db.String(256))
    airport = db.Column(db.String(256))
    park = db.Column(db.String(256))
    point_of_interest = db.Column(db.String(256))




    #main details
    total_area = db.Column(db.Float)
    rooms = db.Column(db.Float)
    bedrooms = db.Column(db.String(128))
    garden_area = db.Column(db.Float)
    state = db.Column(db.String(32))
    status = db.Column(db.String(128))


    #all details

    pool = db.Column(db.String(64))
    garage = db.Column(db.String(64))
    balcony_loggia = db.Column(db.String(64))
    basement = db.Column(db.String(64))
    stockroom = db.Column(db.String(64))
    gas = db.Column(db.String(64))
    water = db.Column(db.String(64))
    central_heating = db.Column(db.String(64))

    #address

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)


    #price and seller
    price = db.Column(db.String(32))
    currency = db.Column(db.String(64))
    price_per_m2 = db.Column(db.String(32))
    seller = db.Column(db.String(64))


    #ფიზიკური პირი, უძრავი ქონების აგენტი, უძრავი ქონების სააგენტო, სამშენებლო კომპანია


    def __repr__(self):
        return f"{self.id}"
