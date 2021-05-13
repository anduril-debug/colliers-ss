from scrapy.item import Item, Field

class LinkItem(Item):
    id = Field()
    link = Field()

class FlatItem(Item):

    id = Field()
    link_id = Field()
    link = Field()
    header = Field()
    city = Field()
    distinct = Field()
    address = Field()
    time = Field()

    #main details
    total_area = Field()
    rooms = Field()
    bedrooms = Field()
    stage = Field()
    total_stages = Field()


    #all details
    balcony_loggia = Field()
    bathtubs = Field()
    project = Field()
    state = Field()
    status = Field()


    #additional information

    garage = Field()
    basement = Field()
    stockroom = Field()
    gas = Field()
    elevator = Field()
    central_heating = Field()

    description = Field()

    #price and seller
    price = Field()
    currency = Field()
    price_per_m2 = Field()
    seller = Field()




class HouseItem(Item):
    id = Field()
    link_id = Field()
    header = Field()
    address = Field()
    code = Field()
    time = Field()

    #main details
    total_area = Field()
    rooms = Field()
    bedrooms = Field()
    garden_area = Field()
    state = Field()
    status = Field()

    #all details
    pool = Field()
    garage = Field()
    balcony_loggia = Field()
    basement = Field()
    stockroom = Field()
    gas = Field()
    water = Field()
    central_heating = Field()


    #price and seller
    price = Field()
    currency = Field()
    price_per_m2 = Field()
    seller = Field()
