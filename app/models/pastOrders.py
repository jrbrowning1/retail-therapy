from flask import current_app as app
from flask_login import current_user
import sys


class pastOrders:
    def __init__(self, oid, uid, total_price, fulfilled, time_purchased, unit_price= None):
        self.oid = oid 
        self.uid = uid
        self.total_price = total_price
        self.fulfilled = fulfilled
        self.time_purchased = time_purchased
        self.unit_price = unit_price

        
    #gets all past orders of user
    @staticmethod
    def get_orders(uid):
        rows = app.db.execute('''
    SELECT *
    FROM Orders
    WHERE uid = :uid
    ORDER BY time_purchased
    DESC
    ''',  
                               uid = uid)
        return [pastOrders(*row) for row in rows] if rows is not None else None

    #gets all products of past user for a specific past order
    @staticmethod
    def get_orderedProducts(uid, oid):
        rows = app.db.execute('''
    SELECT OrderedItems.pid AS pid, name AS name, p_quantity AS p_quantity, unit_price AS unit_price, fulfilled AS fulfilled, fulfillment_time AS fulfillment_time
    FROM OrderedItems, Products
    WHERE uid = :uid AND oid = :oid AND OrderedItems.pid = Products.pid
    ORDER BY pid
    DESC
    ''',  
                               uid = uid, oid=oid)
        return [row for row in rows] if rows is not None else None

    #updates order status if all products are fulfilled
    @staticmethod
    def get_status(uid, orders):
        for order in orders:
            oid = order.oid
            products = pastOrders.get_orderedProducts(uid, oid)
            NonFulfilled = 0
            for item in products:
                fulfilled = item.fulfilled
                if fulfilled == False:
                    NonFulfilled +=1 
            if NonFulfilled == 0:
                rows = app.db.execute('''
    UPDATE Orders
    SET fulfilled = TRUE
    WHERE uid = :uid and oid = :oid
    RETURNING *
    ''',
                                uid = uid, 
                                oid = oid)