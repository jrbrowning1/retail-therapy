from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
import datetime

#import models
from .models.productreview import ProductReview
from .models.prcomment import PR_Comment
from .models.product import Product

from flask import current_app as app

from flask import Blueprint
bp = Blueprint('pr_comments', __name__)

#routes to comments for a particular product review
@bp.route('/pr_comments/product<int:product_number>/user<int:user_id>/<int:number>', methods=['GET', 'POST'])
def ProductReviews(product_number, user_id, number):
    p_reviews = ProductReview.get_all_product_reviews_for_product_and_user(product_number, user_id)
    review_comments = PR_Comment.get_all_product_review_comments(product_number, user_id, number)
    product_name = Product.get_name(product_number)
    total_comments = PR_Comment.get_total_number_product_review_comments(product_number, user_id)
    return render_template('PRComments.html',
                            productreviews = p_reviews,
                            productreviewcomments = review_comments,
                            productname = product_name,
                            number=number,
                            total=total_comments)

#executes review upvote
@bp.route('/pr_comments/product<int:product_number>/user<int:user_id>/upvote', methods=['GET', 'POST'])
def upvote(product_number, user_id):
    PR_Comment.upvote_review(product_number, user_id)
    return redirect(url_for('pr_comments.ProductReviews', product_number = product_number, user_id = user_id, number = 0))

#executes review downvote
@bp.route('/pr_comments/product<int:product_number>/user<int:user_id>/downvote', methods=['GET', 'POST'])
def downvote(product_number, user_id):
    PR_Comment.downvote_review(product_number, user_id)
    return redirect(url_for('pr_comments.ProductReviews', product_number = product_number, user_id = user_id, number = 0))

#executes comment upvote
@bp.route('/pr_comments/product<int:product_number>/user<int:user_id>/upvote_comment/reviewer<int:reviewer_id>', methods=['GET', 'POST'])
def upvote_comment(product_number, user_id, reviewer_id):
    PR_Comment.upvote_comment(product_number, user_id, reviewer_id)
    return redirect(url_for('pr_comments.ProductReviews', product_number = product_number, 
                                                          user_id = user_id, 
                                                          reviewer_id = reviewer_id, 
                                                          number = 0))

#executes comment downvote
@bp.route('/pr_comments/product<int:product_number>/user<int:user_id>/downvote_comment/reviewer<int:reviewer_id>/', methods=['GET', 'POST'])
def downvote_comment(product_number, user_id, reviewer_id):
    PR_Comment.downvote_comment(product_number, user_id, reviewer_id)
    return redirect(url_for('pr_comments.ProductReviews', product_number = product_number, 
                                                          user_id = user_id, 
                                                          reviewer_id = reviewer_id,
                                                          number = 0))

#executes delete comment
@bp.route('/pr_comments/product<int:product_number>/user<int:user_id>/delete_comment/reviewer<int:reviewer_id>', methods=['GET', 'POST'])
def delete_comment(product_number, user_id, reviewer_id):
    PR_Comment.delete_comment(product_number, user_id, reviewer_id)
    return redirect(url_for('pr_comments.ProductReviews', product_number = product_number, 
                                                          user_id = user_id, 
                                                          reviewer_id = reviewer_id,
                                                          number = 0))

#executes delete review
@bp.route('/pr_comments/product<int:product_number>/user<int:user_id>/delete_review', methods=['GET', 'POST'])
def delete_review(product_number, user_id):
    PR_Comment.delete_review(product_number, user_id)
    return redirect(url_for('productreviews.ProductReviews', product_number = product_number, number = 0))