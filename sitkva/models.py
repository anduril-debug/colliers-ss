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
    state = db.Column(db.String(128))
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
    price = db.Column(db.String(128))
    currency = db.Column(db.String(64))
    price_per_m2 = db.Column(db.String(128))
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
    header = db.Column(db.String(256))

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
    state = db.Column(db.String(128))
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
    price = db.Column(db.String(128))
    currency = db.Column(db.String(64))
    price_per_m2 = db.Column(db.String(128))
    seller = db.Column(db.String(64))


    #ფიზიკური პირი, უძრავი ქონების აგენტი, უძრავი ქონების სააგენტო, სამშენებლო კომპანია


    def __repr__(self):
        return f"{self.id}"






class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    districts = db.relationship("District", backref = 'city',cascade="all, delete")

    def __repr__(self):
        return f"{self.name}"


class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    city_id = db.Column(db.Integer, db.ForeignKey("city.id"))
    subdistricts = db.relationship("Subdistrict", backref = 'district',cascade="all, delete")

    def __repr__(self):
        return f"{self.name}"



class Subdistrict(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    district_id = db.Column(db.Integer, db.ForeignKey("district.id"))
    streets = db.relationship("Street", backref = 'subdistrict',cascade="all, delete")

    def __repr__(self):
        return f"{self.name}"


class Street(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    subdistrict_id = db.Column(db.Integer, db.ForeignKey("subdistrict.id"))
    latitude = db.Column(db.String)
    longitude = db.Column(db.String)


    def __repr__(self):
        return f"{self.name}"



class OutsideTbilisi(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128))
    latitude = db.Column(db.String)
    longitude = db.Column(db.String)


    def __repr__(self):
        return f"{self.name}"


class FlatLinkRemodel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    link = db.Column(db.String)
    flat = db.relationship('FlatRemodel', uselist=False, backref = 'flat_link_remodel',cascade="all, delete")
    def __repr__(self):
        return f"id: {self.id}"






class FlatRemodel(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    link_id = db.Column(db.Integer, db.ForeignKey('flat_link_remodel.id',ondelete="CASCADE"))
    header = db.Column(db.String(256))
    time = db.Column(db.String(16))

    #main details
    total_area = db.Column(db.Float)
    rooms = db.Column(db.Float)
    bedrooms = db.Column(db.String(128))
    stage = db.Column(db.Integer)
    total_stages = db.Column(db.Integer)


    administrative_area_level_1 = db.Column(db.String(128))  ###qalaqi - municipaliteti
    administrative_area_level_2 = db.Column(db.String(128))  ###districtebi - soflebi
    administrative_area_level_3 = db.Column(db.String(128))  ### subdistrictebi
    administrative_area_level_4 = db.Column(db.String(128))  ### addressebi


    city = db.Column(db.String(128))
    district = db.Column(db.String(128))
    subdistrict = db.Column(db.String(128))
    address = db.Column(db.String(128))





    #all details
    balcony_loggia = db.Column(db.String(128))
    bathtubs = db.Column(db.String(128))
    project = db.Column(db.String(128))
    state = db.Column(db.String(128))
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


    #price and seller
    price = db.Column(db.String(128))
    currency = db.Column(db.String(64))
    price_per_m2 = db.Column(db.String(128))
    seller = db.Column(db.String(64))


    #ფიზიკური პირი, უძრავი ქონების აგენტი, უძრავი ქონების სააგენტო, სამშენებლო კომპანია


    def __repr__(self):
        return f"{self.id}"




class HouseLinkRemodel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    link = db.Column(db.String)
    house = db.relationship('HouseRemodel', uselist=False, backref = 'house_link_remodel',cascade="all, delete")


    def __repr__(self):
        return f"id: {self.id}"



class HouseRemodel(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    link_id = db.Column(db.Integer, db.ForeignKey('house_link_remodel.id',ondelete="CASCADE"))
    header = db.Column(db.String(256))

    code = db.Column(db.String(256))
    time = db.Column(db.String(16))



    administrative_area_level_1 = db.Column(db.String(128))  ###qalaqi - municipaliteti
    administrative_area_level_2 = db.Column(db.String(128))  ###districtebi - soflebi
    administrative_area_level_3 = db.Column(db.String(128))  ### subdistrictebi
    administrative_area_level_4 = db.Column(db.String(128))  ### addressebi



    city = db.Column(db.String(128))
    district = db.Column(db.String(128))
    subdistrict = db.Column(db.String(128))
    address = db.Column(db.String(128))



    #main details
    total_area = db.Column(db.Float)
    rooms = db.Column(db.Float)
    bedrooms = db.Column(db.String(128))
    garden_area = db.Column(db.Float)
    state = db.Column(db.String(128))
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
    price = db.Column(db.String(128))
    currency = db.Column(db.String(64))
    price_per_m2 = db.Column(db.String(128))
    seller = db.Column(db.String(64))


    #ფიზიკური პირი, უძრავი ქონების აგენტი, უძრავი ქონების სააგენტო, სამშენებლო კომპანია


    def __repr__(self):
        return f"{self.id}"


class AdministrativeArea(db.Model):
    administrative_area_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    latitude = db.Column(db.String(64))
    longitude = db.Column(db.String(64))

    def __repr__(self):
        return f"{self.name}"


class FlatTmpColliersOutsideTbilisi(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.String(16))

    administrative_area_level_1 = db.Column(db.String(128))  ###qalaqi - municipaliteti
    administrative_area_level_2 = db.Column(db.String(128))  ###districtebi - soflebi


    city = db.Column(db.String(128))
    district = db.Column(db.String(128))
    subdistrict = db.Column(db.String(128))
    address = db.Column(db.String(128))



    #main details
    total_area = db.Column(db.Float)
    rooms = db.Column(db.Float)
    bedrooms = db.Column(db.String(128))
    garden_area = db.Column(db.Float)
    state = db.Column(db.String(128))
    status = db.Column(db.String(128))


    #all details


    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)


    #price and seller
    price = db.Column(db.String(128))
    currency = db.Column(db.String(64))
    price_per_m2 = db.Column(db.String(128))


    def __repr__(self):
        return f"{self.id}"


class FlatTmpColliersTbilisi(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.String(16))

    administrative_area_level_1 = db.Column(db.String(128))  ###qalaqi - municipaliteti
    administrative_area_level_2 = db.Column(db.String(128))  ###districtebi - soflebi


    city = db.Column(db.String(128))
    district = db.Column(db.String(128))
    subdistrict = db.Column(db.String(128))
    address = db.Column(db.String(128))



    #main details
    total_area = db.Column(db.Float)
    rooms = db.Column(db.Float)
    bedrooms = db.Column(db.String(128))
    garden_area = db.Column(db.Float)
    state = db.Column(db.String(128))
    status = db.Column(db.String(128))

    #all details


    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)


    #price and seller
    price = db.Column(db.String(128))
    currency = db.Column(db.String(64))
    price_per_m2 = db.Column(db.String(128))


    def __repr__(self):
        return f"{self.id}"
