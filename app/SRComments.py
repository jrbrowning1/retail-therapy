from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
import datetime

#import models
from .models.sellerreview import SellerReview
from .models.srcomment import SR_Comment
from .models.seller import Seller

from flask import current_app as app

from flask import Blueprint
bp = Blueprint('sr_comments', __name__)

@bp.route('/sr_comments/seller<int:seller_id>/user<int:user_id>/<int:number>', methods=['GET', 'POST'])
def SellerReviews(seller_id, user_id, number):
    s_reviews = SellerReview.get_all_seller_reviews_for_seller_and_user(seller_id, user_id)
    review_comments = SR_Comment.get_all_seller_review_comments(seller_id, user_id, number)
    seller_name = Seller.get_seller_info(seller_id)
    total_comments = SR_Comment.get_total_number_seller_review_comments(seller_id, user_id)
    return render_template('SRComments.html',
                            sellerreviews = s_reviews,
                            sellerreviewcomments = review_comments,
                            sellername = seller_name,
                            number = number,
                            total = total_comments)

#executes review upvote
@bp.route('/sr_comments/seller<int:seller_id>/user<int:user_id>/upvote', methods=['GET', 'POST'])
def upvote(seller_id, user_id):
    SR_Comment.upvote_review(seller_id, user_id)
    return redirect(url_for('sr_comments.SellerReviews', seller_id = seller_id, user_id = user_id, number = 0))

#executes review downvote
@bp.route('/sr_comments/seller<int:seller_id>/user<int:user_id>/downvote', methods=['GET', 'POST'])
def downvote(seller_id, user_id):
    SR_Comment.downvote_review(seller_id, user_id)
    return redirect(url_for('sr_comments.SellerReviews', seller_id = seller_id, user_id = user_id, number = 0))

#executes comment upvote
@bp.route('/sr_comments/seller<int:seller_id>/user<int:user_id>/upvote_comment/reviewer<int:reviewer_id>', methods=['GET', 'POST'])
def upvote_comment(seller_id, user_id, reviewer_id):
    SR_Comment.upvote_comment(seller_id, user_id, reviewer_id)
    return redirect(url_for('sr_comments.SellerReviews', seller_id = seller_id, 
                                                         user_id = user_id, 
                                                        reviewer_id = reviewer_id,
                                                        number = 0))

#executes comment downvote
@bp.route('/sr_comments/seller<int:seller_id>/user<int:user_id>/downvote_comment/reviewer<int:reviewer_id>', methods=['GET', 'POST'])
def downvote_comment(seller_id, user_id, reviewer_id):
    SR_Comment.downvote_comment(seller_id, user_id, reviewer_id)
    return redirect(url_for('sr_comments.SellerReviews', seller_id = seller_id, 
                                                         user_id = user_id, 
                                                         reviewer_id = reviewer_id,
                                                         number = 0))

#executes delete comment
@bp.route('/sr_comments/seller<int:seller_id>/user<int:user_id>/delete_comment/reviewer<int:reviewer_id>', methods=['GET', 'POST'])
def delete_comment(seller_id, user_id, reviewer_id):
    SR_Comment.delete_comment(seller_id, user_id, reviewer_id)
    return redirect(url_for('sr_comments.SellerReviews', seller_id = seller_id, 
                                                         user_id = user_id, 
                                                         reviewer_id = reviewer_id,
                                                         number = 0))

#executes delete review
@bp.route('/sr_comments/seller<int:seller_id>/user<int:user_id>/delete_review', methods=['GET', 'POST'])
def delete_review(seller_id, user_id):
    SR_Comment.delete_review(seller_id, user_id)
    return redirect(url_for('sellerreviews.SellerReviews', seller_id = seller_id, number = 0))