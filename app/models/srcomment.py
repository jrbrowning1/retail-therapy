from flask import current_app as app
import sys

#rid = reviewer's user id
#uid = user's id
#seller_id = seller's id
#time_commented generated automatically
#comment input by user
#votes start at 0, can change
class SR_Comment:
    def __init__(self, rid, uid, seller_id, time_commented, comment, votes):
        self.rid = rid
        self.uid = uid
        self.seller_id = seller_id
        self.time_commented = time_commented
        self.comment = comment
        self.votes = votes

#get all comments for particular seller review
    @staticmethod
    def get_all_seller_review_comments(seller_id, uid, number):
        rows = app.db.execute('''
SELECT rid, uid, seller_id, time_commented, comment, votes
FROM SR_Comments
WHERE seller_id = :seller_id AND uid = :uid
ORDER BY time_commented DESC
LIMIT 10
OFFSET :number
''',
                              seller_id=seller_id, uid=uid, number = number)
        return [SR_Comment(*row) for row in rows]

#get number of comments for review
    @staticmethod
    def get_total_number_seller_review_comments(seller_id, uid):
        rows = app.db.execute('''
SELECT rid, uid, seller_id, time_commented, comment, votes
FROM SR_Comments
WHERE seller_id = :seller_id AND uid = :uid
''',
                              seller_id=seller_id, uid=uid)
        return len(rows)

#upvote seller review
    @staticmethod
    def upvote_review(seller_id, uid):
        app.db.execute('''
    UPDATE Seller_Reviews
    SET votes = votes + 1
    WHERE Seller_Reviews.seller_id = :seller_id AND Seller_Reviews.uid = :uid
    RETURNING *;
    ''',  
                               uid = uid, seller_id = seller_id)

#downvote seller review
    @staticmethod
    def downvote_review(seller_id, uid):
        app.db.execute('''
    UPDATE Seller_Reviews
    SET votes = votes - 1
    WHERE Seller_Reviews.seller_id = :seller_id AND Seller_Reviews.uid = :uid
    RETURNING *;
    ''',  
                               uid = uid, seller_id = seller_id)

#upvote comment on seller review
    @staticmethod
    def upvote_comment(seller_id, uid, rid):
        app.db.execute('''
    UPDATE SR_Comments
    SET votes = votes + 1
    WHERE SR_Comments.seller_id = :seller_id AND SR_Comments.uid = :uid AND SR_Comments.rid = :rid
    RETURNING *;
    ''',  
                               uid = uid, seller_id = seller_id, rid = rid)

#downvote comment on seller review
    @staticmethod
    def downvote_comment(seller_id, uid, rid):
        app.db.execute('''
    UPDATE SR_Comments
    SET votes = votes - 1
    WHERE SR_Comments.seller_id = :seller_id AND SR_Comments.uid = :uid AND SR_Comments.rid = :rid
    RETURNING *;
    ''',  
                               uid = uid, seller_id = seller_id, rid = rid)

#add comment to seller review
    @staticmethod
    def addcomment(rid, uid, seller_id, time_commented, comments, votes):
        try:
            print('this is the uid: ' + str(uid), file=sys.stderr)
            print('this is the seller_id: ' + str(seller_id), file = sys.stderr)
            print('this is the time_commented: ' + str(time_commented), file=sys.stderr)
            print('this is the comment: ' + comments, file=sys.stderr)

            rows = app.db.execute("""
INSERT INTO SR_Comments
VALUES(:rid, :uid, :seller_id, :time_commented, :comments, :votes)
RETURNING seller_id
""",
                                  rid = rid,
                                  uid = uid,
                                  seller_id = seller_id,
                                  time_commented = time_commented,
                                  comments = comments,
                                  votes = votes)

            print('seller review comment added!')
            return True
        except Exception:
            print('Error: seller review comment not added', file = sys.stderr)
            return None

#edit comment on seller review
    @staticmethod
    def editcomment(rid, uid, seller_id, time_commented, comment, votes):
        try:
            print('this is the uid: ' + str(uid), file=sys.stderr)
            print('this is the seller_id: ' + str(seller_id), file = sys.stderr)
            print('this is the time_commented: ' + str(time_commented), file=sys.stderr)
            print('this is the comment: ' + comments, file=sys.stderr)

            rows = app.db.execute("""
UPDATE SR_Comments
SET comment = :comment
WHERE rid = :rid AND uid = :uid AND seller_id = :seller_id
RETURNING seller_id
""",
                                  rid = rid,
                                  uid = uid,
                                  seller_id = seller_id,
                                  time_commented = time_commented,
                                  comment = comment,
                                  votes = votes)

            print('seller review comment edited!')
            return True
        except Exception:
            print('Error: seller review comment not edited', file = sys.stderr)
            return None

#delete comment on seller review
    @staticmethod
    def delete_comment(seller_id, uid, rid):
        app.db.execute('''
    DELETE
    FROM SR_Comments
    WHERE seller_id = :seller_id AND uid = :uid AND rid = :rid
    RETURNING *;
    ''',  
                               uid = uid, seller_id = seller_id, rid = rid)

#delete seller review
    @staticmethod
    def delete_review(seller_id, uid):
        app.db.execute('''
    DELETE
    FROM Seller_Reviews
    WHERE seller_id = :seller_id AND uid = :uid
    RETURNING *;
    ''',  
                               uid = uid, seller_id = seller_id)