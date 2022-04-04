from flask import current_app as app
from flask_login import current_user
import sys

#Orders(oid, uid, total_price, fulfilled, time_purchased)
#OrderedItems(oid, pid, total_price, p_quantity, fulfilled, fulfillment_time)

class Order:
    def __init__(oid, uid, total_price, fulfilled, time_purchased, pid, fulfillment_time):
        self.uid = uid
        self.pid = pid
        self.name = name
        self.p_quantity = p_quantity
        self.total_price = total_price
        self.fulfilled = fulfilled
        self.time_purchased = time_purchased 
        self.oid = self.oid
        self.fulfillment_time = fulfillment_time

    #adds order to existing orders of user
    def addToOrders(uid, total_price, time_purchased):
        rows = app.db.execute('''
    SELECT COUNT(uid) FROM Orders
    ''')
        oid = rows[0][0]
        if oid == None:
            oid = 0
        oid = int(oid + 1)

        rows = app.db.execute('''
    INSERT INTO Orders(oid, uid, total_price, fulfilled, time_purchased)
    VALUES (:oid, :uid, :total_price, FALSE, :time_purchased)
    RETURNING oid;
    ''',  
                               uid = uid, total_price = total_price, time_purchased = time_purchased, oid = oid)
        return rows[0][0]

    #adds order to existing orders of seller's products
    def addToSellerOrders(uid, oid, cart_items):
        sellers = set([item.seller_id for item in cart_items])
        rows = []
        for seller in sellers:
            rows = app.db.execute(
                """
                INSERT INTO SellerOrders(seller_id, order_id, uid)
                VALUES (:seller, :oid, :uid)
                RETURNING *
                """, seller=seller, oid=oid, uid=uid
            )
        return rows

    #gets user's balance
    @staticmethod
    def get_balance(uid):
        rows = app.db.execute('''
    SELECT balance FROM Account WHERE uid = :uid''', 
                uid = uid
            )
        user_balance = float(rows[0][0])
        return user_balance

    #checks to see if cart quantity of all items are in stock respectively
    @staticmethod
    def inventory_check(cart_items):

        for item in cart_items:
            uid = item.uid
            pid = item.pid
            name = item.name
            quantity = int(item.p_quantity)
            price = float(item.unit_price)
            seller_id = item.seller_id

            rows = app.db.execute('''
    SELECT in_stock
    FROM Inventory
    WHERE pid = :pid AND seller_id = :seller_id''',
                    pid = pid, seller_id = seller_id)

            num_stock = int(rows[0][0])

            if quantity > num_stock:
                return False

    #decrements the stock for what was just ordered
    @staticmethod
    def update_stock(cart_items):

        for item in cart_items:
            uid = item.uid
            pid = item.pid
            name = item.name
            quantity = int(item.p_quantity)
            price = float(item.unit_price)
            seller_id = item.seller_id

            rows = app.db.execute('''
    UPDATE Inventory
    SET in_stock = in_stock - :quantity
    WHERE pid = :pid AND seller_id = :seller_id
    RETURNING *
                    ''',
                                        pid = pid,
                                        seller_id = seller_id,
                                        quantity = quantity
                )
            print("inventory updated ", name)

    #decrements buyer's baalnce and increment seller's
    @staticmethod
    def update_balances(cart_items, uid, cart_total):
        for item in cart_items:
            uid = item.uid
            pid = item.pid
            name = item.name
            quantity = int(item.p_quantity)
            price = float(item.unit_price)
            seller_id = item.seller_id

            total_price = quantity*price
        
            #Account(uid, balance)
            rows = app.db.execute('''
    UPDATE Account
    SET balance = balance + :total_price
    WHERE uid = :seller_id
    RETURNING balance
                    ''',
                                        seller_id = seller_id,
                                        total_price = total_price)
            #print("seller balance updated:", rows[0][0])
            
    
        rowsb = app.db.execute('''
    UPDATE Account
    SET balance = balance - :cart_total
    WHERE uid = :uid
    RETURNING balance
                    ''',
                                        uid = uid,
                                        cart_total = cart_total)
        #print("buyer balance updated:", rowsb[0][0])

    #empties the cart when the order is placed
    @staticmethod
    def empty_cart(cart_items, uid):
        for item in cart_items:
            uid = item.uid
            pid = item.pid
            name = item.name
            quantity = int(item.p_quantity)
            price = float(item.unit_price)
            seller_id = item.seller_id

            app.db.execute('''
    DELETE
    FROM InCart
    WHERE uid = :uid AND pid = :pid
    RETURNING *
    ''',
                                uid = uid, 
                                pid = pid)
        #print("items deleted from cart")

    #adds all products of order to the history of ordered/puchased items 
    @staticmethod
    def addToOrderedItems(cart_items, uid, oid):
        for item in cart_items:
            uid = item.uid
            pid = item.pid
            name = item.name
            quantity = int(item.p_quantity)
            price = float(item.unit_price)
            seller_id = item.seller_id


            rows = app.db.execute('''
    INSERT INTO OrderedItems 
    VALUES (:uid, :oid, :pid, :unit_price, :quantity, FALSE, NULL)
    RETURNING *;
    ''',  
                               uid = uid, 
                               oid = oid, 
                               pid = pid,
                               unit_price = price,
                               quantity = quantity)
            #print(rows[0])