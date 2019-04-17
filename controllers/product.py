products = []


class Product:
    def __init__(self, json_data):
        self.productId = json_data["productId"] if json_data is not None else None
        self.productName = json_data["productName"] if json_data is not None else None
        self.description = json_data["description"] if json_data is not None else None
        self.price = json_data["price"] if json_data is not None else None
        self.image = json_data["image"] if json_data is not None else None
        products.append(self)

    def getproductid(self):
        return self.productId

    def getproductname(self):
        return self.productName

    def getdescription(self):
        return self.description

    def getprice(self):
        return self.price

    def getimage(self):
        return self.image