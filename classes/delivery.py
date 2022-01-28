import datetime


class Delivery:

    def __init__(self, establishment, product, value):
        self.establishment = establishment
        date = datetime.datetime.now()
        self.product = product
        self.registered_date = date.strftime("%d/%m/%Y")
        self.registered_hour = date.strftime("%H:%M")
        self.value = value
