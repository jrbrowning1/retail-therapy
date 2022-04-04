# from __future__ import print_function # In python 2.7
from flask import render_template
from flask_login import current_user
import datetime

#import forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange

#import models
from .models.productreview import ProductReview
from .models.product import Product

from flask import current_app as app

from flask import Blueprint
bp = Blueprint('productreviews', __name__)

#routes to product reviews page for a certain product
@bp.route('/productreviews/<int:product_number>/<int:number>', methods=['GET', 'POST'])
def ProductReviews(product_number, number):
    p_reviews = ProductReview.get_all_product_reviews_for_product(product_number, number)
    product_review_stats = ProductReview.get_stats(product_number)
    product_name = Product.get_name(product_number)
    PR_check = True
    if current_user.is_authenticated:
        PR_check = ProductReview.review_check(product_number, current_user.uid)
    total_reviews = ProductReview.get_total_number_product_reviews_for_product(product_number)
    return render_template('ProductReviews.html',
                            productreviews = p_reviews,
                            productreviewstats = product_review_stats,
                            productname = product_name,
                            productreviewcheck = PR_check,
                            number = number,
                            total = total_reviews)

