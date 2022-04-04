from flask import current_app as app

import sys

#uid = user's id
#seller_id = seller's id
#time_reviewed gerneated automatically
#rating input by user
#comments input by user
#votes start at 0, can be changed
class SellerReview:
    def __init__(self, uid, seller_id, time_reviewed, rating, comments, votes):
        self.uid = uid
        self.seller_id = seller_id
        self.time_reviewed = time_reviewed
        self.rating = rating
        self.comments = comments
        self.votes = votes

#get all reviews for a seller 
    @staticmethod
    def get_all_seller_reviews_for_seller(seller_id, number):
        rows = app.db.execute('''
SELECT uid, seller_id, time_reviewed, rating, comments, votes
FROM Seller_Reviews
WHERE seller_id = :seller_id
ORDER BY votes DESC, time_reviewed DESC
LIMIT 10
OFFSET :number
''',
                              seller_id=seller_id, number = number)
        return [SellerReview(*row) for row in rows]

#get total number of reviews for a seller 
    @staticmethod
    def get_total_number_seller_reviews_for_seller(seller_id):
        rows = app.db.execute('''
SELECT uid, seller_id, time_reviewed, rating, comments, votes
FROM Seller_Reviews
WHERE seller_id = :seller_id
''',
                              seller_id=seller_id)
        return len(rows)

#get average rating for a seller 
    @staticmethod
    def get_seller_avg_rating(pid):
        rows = app.db.execute('''
SELECT MAX(uid), MAX(seller_id), MAX(time_reviewed), AVG(rating)::numeric(10,2) AS avg, MAX(comments), MAX(votes)
FROM Seller_Reviews
WHERE seller_id = :seller_id
''',
                              seller_id=seller_id)
        return SellerReview(*(rows[0])) if rows else None

#get all review stats for a seller
    @staticmethod
    def get_stats(seller_id):
        rows = app.db.execute('''
SELECT COUNT(uid) AS number, MAX(seller_id) AS seller_id, MAX(time_reviewed), AVG(rating)::numeric(10,2) AS average, MAX(comments), MAX(votes)
FROM Seller_Reviews
WHERE seller_id = :seller_id
''',
                              seller_id=seller_id)
        print(rows[0][3])
        return (rows[0]) if rows else None

#get all reviews of a seller by a user
    @staticmethod
    def get_all_seller_reviews_by_user(uid):
        rows = app.db.execute('''
SELECT uid, seller_id, time_reviewed, rating, comments, votes
FROM Seller_Reviews
WHERE uid = :uid
ORDER BY time_reviewed
''',
                              uid=uid)
        return [SellerReview(*row) for row in rows]

#get all reviews for a certain seller and user
    @staticmethod
    def get_all_seller_reviews_for_seller_and_user(seller_id, uid):
        rows = app.db.execute('''
SELECT uid, seller_id, time_reviewed, rating, comments, votes
FROM Seller_Reviews
WHERE seller_id = :seller_id AND uid = :uid
ORDER BY votes DESC
''',
                              seller_id=seller_id, uid=uid)
        return (rows[0]) if rows else None

#upvote seller review
    @staticmethod
    def upvote_review(seller_id, uid):
        app.db.execute('''
    UPDATE Seller_Reviews
    SET votes = votes + 1
    WHERE Seller_Reviews.seller_id = :seller_id AND Product_Reviews.uid = :uid
    RETURNING *
    ''',  
                               uid = uid, seller_id = seller_id)

#add seller review
    @staticmethod
    def addreview(uid, seller_id, time_reviewed, rating, comments, votes):
        try:
            print('this is the uid: ' + str(uid), file=sys.stderr)
            print('this is the seller_id: ' + str(seller_id), file = sys.stderr)
            print('this is the time_reviewed: ' + str(time_reviewed), file=sys.stderr)
            print('this is the rating: ' + str(rating), file = sys.stderr)
            print('this is the comment: ' + comments, file=sys.stderr)

            rows = app.db.execute("""
INSERT INTO Seller_Reviews
VALUES(:uid, :seller_id, :time_reviewed, :rating, :comments, :votes)
RETURNING seller_id
""",
                                  uid = uid,
                                  seller_id = seller_id,
                                  time_reviewed = time_reviewed,
                                  rating = rating,
                                  comments = comments,
                                  votes = votes)

            print('seller review added!', file = sys.stderr)
            return True
        except Exception:
            print('Error: seller review not added', file = sys.stderr)
            return None


#get average rating for a seller
    def get_just_rating(seller_id):
        rows = app.db.execute('''
SELECT MAX(pid) as seller_id, AVG(rating)::numeric(10,2) AS avg
FROM Seller_Reviews
WHERE seller_id = :seller_id       
''',  
        seller_id = seller_id)
        return (rows[0]) if rows else None

#edit existing seller review
    @staticmethod
    def editreview(uid, seller_id, time_reviewed, rating, comments, votes):
        try:
            print('this is the uid: ' + str(uid), file=sys.stderr)
            print('this is the seller_id: ' + str(seller_id), file = sys.stderr)
            print('this is the time_reviewed: ' + str(time_reviewed), file=sys.stderr)
            print('this is the rating: ' + str(rating), file = sys.stderr)
            print('this is the comment: ' + comments, file=sys.stderr)

            rows = app.db.execute("""
UPDATE Seller_Reviews
SET rating = :rating, comments = :comments
WHERE Seller_Reviews.uid = :uid AND Seller_Reviews.seller_id = :seller_id
RETURNING seller_id
""",
                                  uid = uid,
                                  seller_id = seller_id,
                                  time_reviewed = time_reviewed,
                                  rating = rating,
                                  comments = comments,
                                  votes = votes)

            print('seller review edited!', file = sys.stderr)
            return True
        except Exception:
            print('Error: seller review not edited', file = sys.stderr)
            return None

#checks if user has submitted a review for a seller
    @staticmethod
    def review_check(seller_id, uid):
        rows = app.db.execute('''
        SELECT *
        FROM Seller_Reviews
        WHERE seller_id = :seller_id AND uid = :uid
        ''',
                                seller_id = seller_id, uid = uid)
        return True if rows else False