from scrapy.item import Item, Field


class FlatRemodelItem(Item):

    id = Field()
    link_id = Field()
    link = Field()
    header = Field()
    time = Field()

    city = Field()
    address = Field()

    administrative_area_level_1 = Field()
    administrative_area_level_2 = Field()
    administrative_area_level_3 = Field()
    administrative_area_level_4 = Field()


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



class HouseRemodelItem(Item):
    id = Field()
    link_id = Field()
    header = Field()
    code = Field()
    time = Field()
    address = Field()

    administrative_area_level_1 = Field()
    administrative_area_level_2 = Field()
    administrative_area_level_3 = Field()
    administrative_area_level_4 = Field()



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
