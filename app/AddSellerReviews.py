# from __future__ import print_function # In python 2.7
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
import datetime
import sys

#import forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
from flask_babel import _, lazy_gettext as _l

#import models
from .models.seller import Seller
from .models.sellerreview import SellerReview

from flask import current_app as app

from flask import Blueprint
bp = Blueprint('addsellerreviews', __name__)

#form to add review for a seller
class AddReviewForm(FlaskForm):
    rating = FloatField(_l('Rating'), validators=[DataRequired(), NumberRange(min=0, max=5)])
    comment = TextAreaField(_l('Comment'), validators=[DataRequired()])
    submit = SubmitField(_l('Add Review'))

#routes to form to add a seller review
@bp.route('/addsellerreview/seller<int:sid>/reviewer<int:rid>', methods=['GET', 'POST'])
def addSellerReviews(sid, rid):
    if current_user.is_authenticated:
        form = AddReviewForm()
        print('check 1:user authenticated')
        if form.validate_on_submit():
            print('form validated on submit', file=sys.stderr)
            default_time = datetime.datetime.now()
            default_time = datetime.datetime.strftime(default_time, '%Y-%m-%d %H:%M:%S')
            if SellerReview.addreview(rid,
                                        sid,
                                        default_time,
                                        form.rating.data,
                                        form.comment.data,
                                        0):
                print('seller review added', file=sys.stderr)
                return redirect(url_for('sellerreviews.SellerReviews', seller_id = sid, number = 0))
            else:
                print('Error: seller review not added', file=sys.stderr)
    
    seller_review_stats = SellerReview.get_stats(sid)

    seller_name = Seller.get_seller_info(sid)
    return render_template('addsellerreview.html', title='Add Seller Review', 
                                                    form=form,
                                                    sellerinfo = seller_name,
                                                    sellerreviewstats = seller_review_stats)

#form to edit existing seller review by current user
class EditReviewForm(FlaskForm):
    rating = FloatField(_l('Rating'), validators=[DataRequired(), NumberRange(min=0, max=5)])
    comment = TextAreaField(_l('Comment'), validators=[DataRequired()])
    submit = SubmitField(_l('Edit Review'))

#routes to form to edit existing seller review by current user
@bp.route('/editsellerreview/seller<int:sid>/reviewer<int:rid>', methods=['GET', 'POST'])
def editSellerReviews(sid, rid):
    if current_user.is_authenticated:
        form = EditReviewForm()
        print('check 1: user authenticated')
        if form.validate_on_submit():
            print('form validated on submit', file=sys.stderr)
            default_time = datetime.datetime.now()
            default_time = datetime.datetime.strftime(default_time, '%Y-%m-%d %H:%M:%S')
            if SellerReview.editreview(rid,
                                        sid,
                                        default_time,
                                        form.rating.data,
                                        form.comment.data,
                                        0):
                print('seller review updated', file=sys.stderr)
                return redirect(url_for('sellerreviews.SellerReviews', seller_id = sid, number = 0))
            else:
                print('Error: seller review not updated', file=sys.stderr)
    
    seller_review_stats = SellerReview.get_stats(sid)

    seller_name = Seller.get_seller_info(sid)
    return render_template('editsellerreview.html', title='Edit Seller Review', 
                                                    form=form,
                                                    sellerinfo = seller_name,
                                                    sellerreviewstats = seller_review_stats)