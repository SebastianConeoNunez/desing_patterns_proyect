class Product:
    def __init__(self):
        self.id = None
        self.name = None
        self.category = None
        self.price = None

    def set_id(self, id: int):
        self.id = id
        return self
    
    def set_name(self, name: str):
        self.name = name
        return self

    def set_category(self, category: str):
        self.category = category
        return self

    def set_price(self, price: float):
        self.price = price
        return self
    
    def build(self):
        if not self.name:
            raise ValueError("Product must have a name.")
        if not self.category:
            raise ValueError("Product must have a category.")
        if self.price is None:
            raise ValueError("Product must have a price.")
        if self.price < 0:
            raise ValueError("Price cannot ser negativo.")

        return self

    def __repr__(self):
        return f"<Product name={self.name}, category={self.category}, price={self.price}>"
