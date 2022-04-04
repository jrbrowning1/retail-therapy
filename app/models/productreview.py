from flask import current_app as app

import sys

#uid = user's id
#pid = product id
#time_reviewed is generated automatically
#rating is a float between 0 and 5, input by user
#comments are input by user
#votes start at 0, can be changed
class ProductReview:
    def __init__(self, uid, pid, time_reviewed, rating, comments, votes):
        self.uid = uid
        self.pid = pid
        self.time_reviewed = time_reviewed
        self.rating = rating
        self.comments = comments
        self.votes = votes

#get all product reviews for a product        
    @staticmethod
    def get_all_product_reviews_for_product(pid, number):
        rows = app.db.execute('''
SELECT uid, pid, time_reviewed, rating, comments, votes
FROM Product_Reviews
WHERE pid = :pid
ORDER BY votes DESC, time_reviewed DESC
LIMIT 10
OFFSET :number
''',
                              pid=pid, number = number)
        return [ProductReview(*row) for row in rows]

#get total number of product reviews for product
    @staticmethod
    def get_total_number_product_reviews_for_product(pid):
        rows = app.db.execute('''
SELECT uid, pid, time_reviewed, rating, comments, votes
FROM Product_Reviews
WHERE pid = :pid
''',
                              pid=pid)
        return len(rows)

#get all review stats associated with a product
    @staticmethod
    def get_stats(pid):
        rows = app.db.execute('''
SELECT COUNT(uid) AS number, MAX(pid) AS pid, MAX(time_reviewed), AVG(rating)::numeric(10,2) AS average, MAX(comments), MAX(votes)
FROM Product_Reviews
WHERE pid = :pid
''',
                              pid=pid)
        print(rows[0][3])
        return (rows[0]) if rows else None

#get all product reviews by a certain user
    @staticmethod
    def get_all_product_reviews_by_user(uid):
        rows = app.db.execute('''
SELECT uid, pid, time_reviewed, rating, comments, votes
FROM Product_Reviews
WHERE uid = :uid
ORDER BY time_reviewed DESC
''',
                              uid=uid)
        return [ProductReview(*row) for row in rows]

#get all product reviews for a certain product written by a certain user
    @staticmethod
    def get_all_product_reviews_for_product_and_user(pid, uid):
        rows = app.db.execute('''
SELECT uid, pid, time_reviewed, rating, comments, votes
FROM Product_Reviews
WHERE pid = :pid AND uid = :uid
ORDER BY votes DESC
''',
                              pid=pid, uid=uid)
        return (rows[0]) if rows else None

#add product review
    @staticmethod
    def addreview(uid, pid, time_reviewed, rating, comments, votes):
        try:
            print('this is the uid: ' + str(uid), file=sys.stderr)
            print('this is the pid: ' + str(pid), file = sys.stderr)
            print('this is the time_reviewed: ' + str(time_reviewed), file=sys.stderr)
            print('this is the rating: ' + str(rating), file = sys.stderr)
            print('this is the comment: ' + comments, file=sys.stderr)

            rows = app.db.execute("""
INSERT INTO Product_Reviews
VALUES(:uid, :pid, :time_reviewed, :rating, :comments, :votes)
RETURNING pid
""",
                                  uid = uid,
                                  pid = pid,
                                  time_reviewed = time_reviewed,
                                  rating = rating,
                                  comments = comments,
                                  votes = votes)

            print('product review added!', file = sys.stderr)
            return True
        except Exception:
            print('Error: product review not added', file = sys.stderr)
            return None

#get rating for a product
    def get_just_rating(pid):
        rows = app.db.execute('''
SELECT MAX(pid) as pid, AVG(rating)::numeric(10,2) AS avg
FROM Product_Reviews
WHERE pid = :pid        
''',  
        pid = pid)
        return (rows[0]) if rows else None

#edit existing product review
    @staticmethod
    def editreview(uid, pid, time_reviewed, rating, comments, votes):
        try:
            print('this is the uid: ' + str(uid), file=sys.stderr)
            print('this is the pid: ' + str(pid), file = sys.stderr)
            print('this is the time_reviewed: ' + str(time_reviewed), file=sys.stderr)
            print('this is the rating: ' + str(rating), file = sys.stderr)
            print('this is the comment: ' + comments, file=sys.stderr)

            rows = app.db.execute("""
UPDATE Product_Reviews
SET time_reviewed = :time_reviewed, rating = :rating, comments = :comments
WHERE Product_Reviews.uid = :uid AND Product_Reviews.pid = :pid
RETURNING *
""",
                                  uid = uid,
                                  pid = pid,
                                  time_reviewed = time_reviewed,
                                  rating = rating,
                                  comments = comments,
                                  votes = votes)

            print('product review edited!', file = sys.stderr)
            return True
        except Exception:
            print('Error: product review not edited', file = sys.stderr)
            return None

#check that a user has not already added a review for a product
    @staticmethod
    def review_check(pid, uid):
        rows = app.db.execute('''
        SELECT *
        FROM Product_Reviews
        WHERE pid = :pid AND uid = :uid
        ''',
                                uid = uid, pid = pid)
        return True if rows else False