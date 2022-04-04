from flask import current_app as app
from flask_login import current_user

import sys

from .. import login

class Account:
    def __init__(self, uid, balance):
        self.uid = uid
        self.balance = balance

    def get_id(self):
        return (self.uid)

    @staticmethod
    def update_balance(uid, balance):
        try:
            rows = app.db.execute("""
UPDATE Account
SET  balance = balance + :balance
WHERE uid = :uid
RETURNING *
""",
                                  uid=uid,
                                  balance=balance)
            print('balance updated', file = sys.stderr)
            return True
        except Exception:
            print('bad things happening', file = sys.stderr)
            return None


    @staticmethod
    def get_balance(uid):
        rows = app.db.execute("""
SELECT *
FROM Account
WHERE uid = :uid
""",
                              uid=uid)
        return round(rows[0][1], 2) if rows else 0.00
