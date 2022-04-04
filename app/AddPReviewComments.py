# from __future__ import print_function # In python 2.7
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
import datetime
import sys

#import forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FloatField, DateTimeField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
from flask_babel import _, lazy_gettext as _l

#import models
from .models.productreview import ProductReview
from .models.product import Product
from .models.prcomment import PR_Comment

from flask import current_app as app

from flask import Blueprint
bp = Blueprint('addpreviewcomments', __name__)

#Form to add comment to a particular review of a product
class AddCommentForm(FlaskForm):
    comment = TextAreaField(_l('Comment'), validators=[DataRequired()])
    submit = SubmitField(_l('Add Comment'))

#routes to the page to add a comment to a particular product review page
@bp.route('/addpr_comment/product<int:pid>/user<int:uid>/reviewer<int:rid>', methods=['GET', 'POST'])
def addProductReviews(pid, uid, rid):
    if current_user.is_authenticated:
        form = AddCommentForm()
        print('check 1')
        if form.validate_on_submit():
            print('form validated on submit', file=sys.stderr)
            default_time = datetime.datetime.now()
            default_time = datetime.datetime.strftime(default_time, '%Y-%m-%d %H:%M:%S')
            if PR_Comment.addcomment(rid,
                                        uid,
                                        pid,
                                        default_time,
                                        form.comment.data,
                                        0):
                print('comment was added', file=sys.stderr)
                return redirect(url_for('pr_comments.ProductReviews', product_number = pid, user_id = uid, number = 0))
            else:
                print('Error: comment was not added', file=sys.stderr)
    
    p_reviews = ProductReview.get_all_product_reviews_for_product_and_user(pid, uid)

    product_review_stats = ProductReview.get_stats(pid)

    product_name = Product.get_name(pid)
    return render_template('addproductreviewcomment.html', title='Add Comment', 
                                                    form=form,
                                                    productname = product_name,
                                                    productreviews = p_reviews)

#form to edit an existing comment by the current user
class EditCommentForm(FlaskForm):
    comment = TextAreaField(_l('Comment'), validators=[DataRequired()])
    submit = SubmitField(_l('Edit Comment'))

#routes to page to submit form to edit an existing comment for a particular product review
@bp.route('/editpr_comment/product<int:pid>/user<int:uid>/reviewer<int:rid>', methods=['GET', 'POST'])
def editProductReviews(pid, uid, rid):
    if current_user.is_authenticated:
        form = EditCommentForm()
        print('check 1: user authenticated')
        if form.validate_on_submit():
            print('form validated', file=sys.stderr)
            default_time = datetime.datetime.now()
            default_time = datetime.datetime.strftime(default_time, '%Y-%m-%d %H:%M:%S')
            if PR_Comment.editcomment(rid,
                                        uid,
                                        pid,
                                        default_time,
                                        form.comment.data,
                                        0):
                print('comment updated', file=sys.stderr)
                return redirect(url_for('pr_comments.ProductReviews', product_number = pid, user_id = uid, number = 0))
            else:
                print('Error: comment was not updated', file=sys.stderr)
    
    p_reviews = ProductReview.get_all_product_reviews_for_product_and_user(pid, uid)

    product_review_stats = ProductReview.get_stats(pid)

    product_name = Product.get_name(pid)
    return render_template('editproductreviewcomment.html', title='Edit Comment', 
                                                    form=form,
                                                    productname = product_name,
                                                    productreviews = p_reviews)

