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
from .models.sellerreview import SellerReview
from .models.seller import Seller
from .models.srcomment import SR_Comment

from flask import current_app as app

from flask import Blueprint
bp = Blueprint('addsreviewcomments', __name__)

#form to add comment to a particular seller review
class AddCommentForm(FlaskForm):
    comment = TextAreaField(_l('Comment'), validators=[DataRequired()])
    submit = SubmitField(_l('Add Comment'))

#routes to form to add comment to a particular seller review
@bp.route('/addsr_comment/seller<int:seller_id>/user<int:uid>/reviewer<int:rid>', methods=['GET', 'POST'])
def addSellerReviews(seller_id, uid, rid):
    if current_user.is_authenticated:
        form = AddCommentForm()
        print('check 1: user authenticated')
        if form.validate_on_submit():
            print('form validated on submit', file=sys.stderr)
            default_time = datetime.datetime.now()
            default_time = datetime.datetime.strftime(default_time, '%Y-%m-%d %H:%M:%S')
            if SR_Comment.addcomment(rid,
                                        uid,
                                        seller_id,
                                        default_time,
                                        form.comment.data,
                                        0):
                print('comment added', file=sys.stderr)
                return redirect(url_for('sr_comments.SellerReviews', seller_id = seller_id, user_id = uid, number = 0))
            else:
                print('Error: comment not added', file=sys.stderr)
    
    s_reviews = SellerReview.get_all_seller_reviews_for_seller_and_user(seller_id, uid)

    seller_review_stats = SellerReview.get_stats(seller_id)

    seller_name = Seller.get_seller_info(seller_id)
    return render_template('addsellerreviewcomment.html', title='Add Comment', 
                                                    form=form,
                                                    sellername = seller_name,
                                                    sellerreviews = s_reviews)

#form to edit existing comment on seller review
class EditCommentForm(FlaskForm):
    comment = TextAreaField(_l('Comment'), validators=[DataRequired()])
    submit = SubmitField(_l('Edit Comment'))

#routes to form to edit existing comment on seller review
@bp.route('/editsr_comment/seller<int:seller_id>/user<int:uid>/reviewer<int:rid>', methods=['GET', 'POST'])
def editSellerReviews(seller_id, uid, rid):
    if current_user.is_authenticated:
        form = EditCommentForm()
        print('check 1: user authenticated')
        if form.validate_on_submit():
            print('form validated on submit', file=sys.stderr)
            default_time = datetime.datetime.now()
            default_time = datetime.datetime.strftime(default_time, '%Y-%m-%d %H:%M:%S')
            if SR_Comment.editcomment(rid,
                                        uid,
                                        seller_id,
                                        default_time,
                                        form.comment.data,
                                        0):
                print('seller review comment updated', file=sys.stderr)
                return redirect(url_for('sr_comments.SellerReviews', seller_id = seller_id, user_id = uid, number = 0))
            else:
                print('Error: seller review comment not updated', file=sys.stderr)
    
    s_reviews = SellerReview.get_all_seller_reviews_for_seller_and_user(seller_id, uid)

    seller_review_stats = SellerReview.get_stats(seller_id)

    seller_name = Seller.get_seller_info(seller_id)
    return render_template('editsellerreviewcomment.html', title='Edit Comment', 
                                                    form=form,
                                                    sellername = seller_name,
                                                    sellerreviews = s_reviews)
