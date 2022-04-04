from flask import current_app as app
import sys

#rid = reviewer's user id
#uid = user's id
#pid = product id
#time_commented generated automatically
#comment input by user
#votes start at 0, can change
class PR_Comment:
    def __init__(self, rid, uid, pid, time_commented, comment, votes):
        self.rid = rid
        self.uid = uid
        self.pid = pid
        self.time_commented = time_commented
        self.comment = comment
        self.votes = votes

#get all comments for a particular product review
    @staticmethod
    def get_all_product_review_comments(pid, uid, number):
        rows = app.db.execute('''
SELECT rid, uid, pid, time_commented, comment, votes
FROM PR_Comments
WHERE pid = :pid AND uid = :uid
ORDER BY time_commented DESC
LIMIT 10
OFFSET :number
''',
                              pid=pid, uid=uid, number=number)
        return [PR_Comment(*row) for row in rows]

#get number of comments for review
    @staticmethod
    def get_total_number_product_review_comments(pid, uid):
        rows = app.db.execute('''
SELECT rid, uid, pid, time_commented, comment, votes
FROM PR_Comments
WHERE pid = :pid AND uid = :uid
''',
                              pid=pid, uid=uid)
        return len(rows)

#upvote product review
    @staticmethod
    def upvote_review(pid, uid):
        app.db.execute('''
    UPDATE Product_Reviews
    SET votes = votes + 1
    WHERE Product_Reviews.pid = :pid AND Product_Reviews.uid = :uid
    RETURNING *;
    ''',  
                               uid = uid, pid = pid)
        print('review upvoted!', file = sys.stderr)

#downvote product review
    @staticmethod
    def downvote_review(pid, uid):
        app.db.execute('''
    UPDATE Product_Reviews
    SET votes = votes - 1
    WHERE Product_Reviews.pid = :pid AND Product_Reviews.uid = :uid
    RETURNING *;
    ''',  
                               uid = uid, pid = pid)
        print('review downvoted!', file = sys.stderr)

#upvote comment on product review
    @staticmethod
    def upvote_comment(pid, uid, rid):
        app.db.execute('''
    UPDATE PR_Comments
    SET votes = votes + 1
    WHERE PR_Comments.pid = :pid AND PR_Comments.uid = :uid AND PR_Comments.rid = :rid
    RETURNING *;
    ''',  
                               uid = uid, pid = pid, rid = rid)
        print('comment upvoted!', file = sys.stderr)

#downvote comment on product review
    @staticmethod
    def downvote_comment(pid, uid, rid):
        app.db.execute('''
    UPDATE PR_Comments
    SET votes = votes - 1
    WHERE PR_Comments.pid = :pid AND PR_Comments.uid = :uid AND PR_Comments.rid = :rid
    RETURNING *;
    ''',  
                               uid = uid, pid = pid, rid = rid)
        print('comment downvoted!', file = sys.stderr)

#add comment on product review
    @staticmethod
    def addcomment(rid, uid, pid, time_commented, comment, votes):
        try:
            print('this is the rid: ' + str(rid), file=sys.stderr)
            print('this is the uid: ' + str(uid), file=sys.stderr)
            print('this is the pid: ' + str(pid), file = sys.stderr)
            print('this is the time_commented: ' + str(time_commented), file=sys.stderr)
            print('this is the comment: ' + comment, file=sys.stderr)

            rows = app.db.execute("""
INSERT INTO PR_Comments
VALUES(:rid, :uid, :pid, :time_commented, :comment, :votes)
RETURNING pid
""",
                                  rid = rid,
                                  uid = uid,
                                  pid = pid,
                                  time_commented = time_commented,
                                  comment = comment,
                                  votes = votes)
            print('commend added!')
            return True
        except Exception:
            print('Error: comment not added', file = sys.stderr)
            return None

#edit existing comment on product review
    @staticmethod
    def editcomment(rid, uid, pid, time_commented, comment, votes):
        try:
            print('this is the rid: ' + str(rid), file=sys.stderr)
            print('this is the uid: ' + str(uid), file=sys.stderr)
            print('this is the pid: ' + str(pid), file = sys.stderr)
            print('this is the time_commented: ' + str(time_commented), file=sys.stderr)
            print('this is the comment: ' + comment, file=sys.stderr)
            
            rows = app.db.execute("""
UPDATE PR_Comments
SET time_commented = :time_commented, comment = :comment
WHERE uid = :uid AND pid = :pid AND rid = :rid
RETURNING *
""",
                                  rid = rid,
                                  uid = uid,
                                  pid = pid,
                                  time_commented = time_commented,
                                  comment = comment,
                                  votes = votes)

            print('comment edited!', file = sys.stderr)
            return True
        except Exception:
            print('Error: comment not edited', file = sys.stderr)
            return None

#delete existing comment on product review
    @staticmethod
    def delete_comment(pid, uid, rid, time_commented):
        app.db.execute('''
    DELETE
    FROM PR_Comments
    WHERE pid = :pid AND uid = :uid AND rid = :rid AND time_commented = :time_commented
    RETURNING *;
    ''',  
                               uid = uid, pid = pid, rid = rid, time_commented = time_commented)
        print('comment deleted', file=sys.stderr)

#delete product review
    @staticmethod
    def delete_review(pid, uid):
        app.db.execute('''
    DELETE
    FROM Product_Reviews
    WHERE pid = :pid AND uid = :uid
    RETURNING *;
    ''',  
                               uid = uid, pid = pid)
        print('review deleted', file=sys.stderr)