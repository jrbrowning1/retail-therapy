from flask import current_app as app
from flask_login import current_user
import datetime


class Seller:
    def __init__(self, uid):
        self.uid = uid

    
    @staticmethod
    def get_seller_products(uid):
        # gets all the products in the inventory of a seller
        rows = app.db.execute("""
        SELECT  Inventory.pid AS pid,
                Products.name AS name,
                Products.price AS price,
                Products.available AS available,
                Inventory.in_stock AS in_stock
        FROM Inventory, Products
        WHERE seller_id = :uid AND Inventory.pid = Products.pid
        """, uid=uid)

        return [row for row in rows]

    @staticmethod
    def get_seller_info(uid):
        # gets profile info of a seller
        rows = app.db.execute("""
        SELECT *
        FROM Users
        WHERE uid = :uid
        """, uid=uid)

        return (rows[0]) if rows else None
    
    @staticmethod
    def get_seller_orders(uid):
        # gets relevant order information for a seller
        rows = app.db.execute("""
        SELECT  Orders.oid AS oid,
                OrderedItems.pid AS pid,
                Users.address AS shipping_address,
                Orders.time_purchased AS purchase_date,
                OrderedItems.fulfilled AS status
        FROM Orders, SellerOrders, Users, OrderedItems
        WHERE SellerOrders.seller_id=:uid
                AND Orders.oid=OrderedItems.oid
                ANd SellerOrders.order_id=Orders.oid
                AND Orders.uid=Users.uid
                AND pid IN (SELECT Inventory.pid FROM Inventory WHERE Inventory.seller_id=:uid )
        """, uid=uid)
        return [row for row in rows]

    @staticmethod
    def add_to_inventory(productname, price, quantity, description, image, category):
        # adds a new product to inventory
        available = False
        if quantity > 0:
            available = True
        sid = current_user.uid
        # product id of new product should be 1 greater than the current max product id
        new_pid = app.db.execute(
        """
        SELECT MAX(pid)
        FROM Products
        """)[0][0] + 1
        try:
            app.db.execute( # add to Products
                """
                INSERT INTO Products(pid, name, price, available, image, description, category)
                VALUES(:new_pid, :productname, :price, :available, :image, :description, :category)
                RETURNING pid
                """, new_pid=new_pid, productname=productname, price=price, available=available, description=description, image=image, category=category)
            app.db.execute( # add to Inventory
                """
                INSERT INTO Inventory(seller_id, pid, in_stock)
                VALUES(:sid, :new_pid, :quantity)
                RETURNING pid
                """, sid=sid, new_pid=new_pid, quantity=quantity
            )
            return 1
        except Exception:
            return 0

    @staticmethod
    def edit_in_inventory(pid, productname, price, quantity, description, image, category):
        # edits an entry that is currently in inventory and products
        available = False
        if quantity > 0:
            available = True
        sid = current_user.uid
        try:
            app.db.execute( # update Products
                """
                UPDATE Products
                SET name=:productname, price=:price, available=:available, description=:description, image=:image, category=:category
                WHERE pid = :pid
                RETURNING pid
                """, pid=pid, productname=productname, price=price, available=available, description=description, image=image, category=category)
            app.db.execute( # update Inventory
                """
                UPDATE Inventory
                SET in_stock=:quantity
                WHERE pid=:pid
                RETURNING pid
                """, sid=sid, pid=pid, quantity=quantity
            )
            return 1
        except Exception as e:
            return 0

    @staticmethod
    def delete_from_inventory(pid):
        # deletes an item from inventory and products tables
        try:
            app.db.execute(
                """
                DELETE FROM Inventory
                WHERE pid = :pid
                """, pid=pid
            )
            app.db.execute(
                """
                DELETE FROM Products
                WHERE pid = :pid
                """, pid=pid
            )
            return 1
        except Exception as e:
            return 0
    
    @staticmethod
    def get_choices():
        # gets all the available categories that a product can be, sorted alphabetically
        try:
            rows = app.db.execute("""
            SELECT DISTINCT category
            FROM Products
            """)
            return sorted([(row[0], row[0]) for row in rows]) if rows else None
        except Exception:
            return 0
    
    @staticmethod
    def mark_item_fulfilled(oid, pid):
        # marks an item in an order as fulfilled
        time = datetime.datetime.now()
        rows = app.db.execute(
            """
            UPDATE OrderedItems
            SET fulfilled=TRUE, fulfillment_time=:time
            WHERE oid=:oid AND pid=:pid
            RETURNING *
            """, oid=oid, pid=pid, time=time
        )
        return rows
