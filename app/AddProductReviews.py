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
from .models.productreview import ProductReview
from .models.product import Product

from flask import current_app as app

from flask import Blueprint
bp = Blueprint('addproductreviews', __name__)


#form to add review for a product
class AddReviewForm(FlaskForm):
    rating = FloatField(_l('Rating'), validators=[DataRequired(), NumberRange(min=0, max=5)])
    comment = TextAreaField(_l('Comment'), validators=[DataRequired()])
    submit = SubmitField(_l('Add Review'))


#routes to form to add a product review
@bp.route('/addproductreview/product<int:pid>/reviewer<int:rid>', methods=['GET', 'POST'])
def addProductReviews(pid, rid):
    if current_user.is_authenticated:
        form = AddReviewForm()
        print('check 1: user authenticated')
        if form.validate_on_submit():
            print('form validated', file=sys.stderr)
            default_time = datetime.datetime.now()
            default_time = datetime.datetime.strftime(default_time, '%Y-%m-%d %H:%M:%S')
            if ProductReview.addreview(rid,
                                        pid,
                                        default_time,
                                        form.rating.data,
                                        form.comment.data,
                                        0):
                print('review added', file=sys.stderr)
                return redirect(url_for('productreviews.ProductReviews', product_number = pid, number = 0))
            else:
                print('Error: review not added', file=sys.stderr)
    
    product_review_stats = ProductReview.get_stats(pid)

    product_name = Product.get_name(pid)
    return render_template('addproductreview.html', title='Add Product Review', 
                                                    form=form,
                                                    productname = product_name,
                                                    productreviewstats = product_review_stats)

#form to edit an existing review by the current user
class EditReviewForm(FlaskForm):
    rating = FloatField(_l('Rating'), validators=[DataRequired(), NumberRange(min=0, max=5)])
    comment = TextAreaField(_l('Comment'), validators=[DataRequired()])
    submit = SubmitField(_l('Add Review'))

#routes to form to edit an existing review
@bp.route('/editproductreview/product<int:pid>/reviewer<int:rid>', methods=['GET', 'POST'])
def editProductReviews(pid, rid):
    if current_user.is_authenticated:
        form = EditReviewForm()
        print('check 1: user authenticated')
        if form.validate_on_submit():
            print('form validated on submit', file=sys.stderr)
            default_time = datetime.datetime.now()
            default_time = datetime.datetime.strftime(default_time, '%Y-%m-%d %H:%M:%S')
            if ProductReview.editreview(rid,
                                        pid,
                                        default_time,
                                        form.rating.data,
                                        form.comment.data,
                                        0):
                print('review updated', file=sys.stderr)
                return redirect(url_for('productreviews.ProductReviews', product_number = pid, number = 0))
            else:
                print('Error: review not updated', file=sys.stderr)
    
    product_review_stats = ProductReview.get_stats(pid)

    product_name = Product.get_name(pid)
    return render_template('editproductreview.html', title='Edit Product Review', 
                                                    form=form,
                                                    productname = product_name,
                                                    productreviewstats = product_review_stats)