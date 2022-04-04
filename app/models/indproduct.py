from flask import current_app as app

# individual product class
class OneProduct:
    def __init__(self, pid, name, price, available, img):
        self.pid = pid
        self.name = name
        self.price = price
        self.available = available
        self.img = img

    # get all basic info related to this product and return it
    @staticmethod
    def get_all_product_info(pid):
        rows = app.db.execute('''
SELECT pid, name, price, available, img
FROM Products
WHERE pid = :pid          
''',
                        pid=pid)
        return [OneProduct(*(rows[0])) if rows is not None else None]