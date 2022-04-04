from flask import current_app as app


class Purchase:
    def __init__(self, oid, uid, time_purchased, total_amount, item_quantity, fulfillment_status, order_page):
        self.oid = oid
        self.uid = uid
        self.time_purchased = time_purchased
        self.total_amount = total_amount
        self.item_quantity = item_quantity
        self.fulfillment_status = fulfillment_status
        self.order_page = order_page

#     @staticmethod
#     def get(id):
#         rows = app.db.execute('''
# SELECT id, uid, pid, time_purchased
# FROM Purchases
# WHERE id = :id
# ''',
#                               id=id)
#         return Purchase(*(rows[0])) if rows else None

#     @staticmethod
#     def get_all_by_uid_since(uid, since):
#         rows = app.db.execute('''
# SELECT id, uid, pid, time_purchased
# FROM Purchases
# WHERE uid = :uid
# AND time_purchased >= :since
# ORDER BY time_purchased DESC
# ''',
#                               uid=uid,
#                               since=since)
#         return [Purchase(*row) for row in rows]
