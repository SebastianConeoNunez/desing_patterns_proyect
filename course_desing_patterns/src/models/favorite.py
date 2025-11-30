class Favorite:
    def __init__(self):
        self.user_id = None
        self.product_id = None

    def set_user_id(self, user_id: int):
        self.user_id = user_id
        return self

    def set_product_id(self, product_id: int):
        self.product_id = product_id
        return self

    def build(self):
        if self.user_id is None:
            raise ValueError("Favorite must have a user_id.")
        if self.product_id is None:
            raise ValueError("Favorite must have a product_id.")

        return self

    def __repr__(self):
        return f"<Favorite user_id={self.user_id}, product_id={self.product_id}>"
