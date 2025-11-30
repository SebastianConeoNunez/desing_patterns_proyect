class Category:
    def __init__(self):
        self.id = None
        self.name = None
      

    def set_id(self, id: int):
        self.id = id
        return self
    
    def set_name(self, name: str):
        self.name = name
        return self

   
    def build(self):
        if not self.name:
            raise ValueError("Product must have a name.")

        return self

    def __repr__(self):
        return f"<Category name={self.name}>"
