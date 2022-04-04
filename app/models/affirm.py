from flask import current_app as app
from flask_login import current_user
import sys


class Affirm:
    def __init__(self, affirmation):
        self.affirmation = affirmation

    @staticmethod
    def add_affirmation(affirmation):
 #       rows = app.db.execute("""
#INSERT INTO Affirm (affirmation)
#VALUES (:affirmation)
#RETURNING *
#""",

        try:
            app.db.execute( # add to Products
                """
INSERT INTO Affirm (affirmation)
VALUES (:affirmation)
RETURNING *
""", affirmation=affirmation)
            print("query ran")
            return 1
        except Exception as e:
            print("Something went wrong")
            print(str(e))
                                  

    @staticmethod
    def get_affirmations():
        rows = app.db.execute("""
SELECT *
FROM Affirm
""",)
        print("get is running")
        return (row for row in rows) if rows is not None else None