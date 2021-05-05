from scrapy.item import Item, Field

class FlatLinkItem(Item):
    id = Field()
    link = Field()

class FlatItem(Item):

    id = Field()
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
