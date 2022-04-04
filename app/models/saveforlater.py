from flask import current_app as app
from flask_login import current_user



class Later:
    def __init__(self, uid, pid, name, p_quantity, unit_price, seller_id):
        self.uid = uid
        self.pid = pid
        self.name = name
        self.p_quantity = p_quantity
        self.unit_price = unit_price
        self.seller_id = seller_id
    
    #gets all items in Save For Later for the user
    @staticmethod
    def get_cart(uid):
        rows = app.db.execute('''
SELECT uid, pid, name, p_quantity, unit_price, seller_id
FROM SaveForLater
WHERE uid = :uid
ORDER BY pid
''',
                              uid=uid)
        print("got sfl data")
        print([row for row in rows])
        return [row for row in rows] if rows is not None else None

    #adds product from cart to save for later
    @staticmethod
    def add(pid, uid):
        rows = app.db.execute('''
    INSERT INTO SaveForLater 
    SELECT :uid, :pid, name, 1, price, seller_id
    FROM Products, Inventory
    WHERE Products.pid = :pid AND Products.pid = Inventory.pid AND Inventory.in_stock > 0
    LIMIT 1
    RETURNING *;
    ''',  
                               uid = uid, pid = pid)
        print([row for row in rows])
    
    #checks to see if product is already in save for later
    @staticmethod
    def check(pid, uid):
        rows = app.db.execute('''
    SELECT * 
    FROM SaveForLater
    WHERE uid = :uid AND pid = :pid
    ''',
                                uid = uid, 
                                pid = pid)

        if len(rows) == 0:
            return False
        else:
            return True 

    #removes product from save for later
    @staticmethod
    def remove(pid, uid):
        app.db.execute('''
    DELETE
    FROM SaveForLater
    WHERE uid = :uid AND pid = :pid
    RETURNING *
    ''',
                                uid = uid, 
                                pid = pid)
