# from __future__ import print_function # In python 2.7
from flask import render_template
from flask_login import current_user
import datetime

#import forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange

#import models
from .models.sellerreview import SellerReview
from .models.seller import Seller

from flask import current_app as app

from flask import Blueprint
bp = Blueprint('sellerreviews', __name__)

#routes to reviews page for certain seller
@bp.route('/sellerreviews/<int:seller_id>/<int:number>', methods=['GET', 'POST'])
def SellerReviews(seller_id, number):
    s_reviews = SellerReview.get_all_seller_reviews_for_seller(seller_id, number)
    seller_review_stats = SellerReview.get_stats(seller_id)
    seller_name = Seller.get_seller_info(seller_id)
    SR_check = True
    if current_user.is_authenticated:
        SR_check = SellerReview.review_check(seller_id, current_user.uid)
    total_reviews = SellerReview.get_total_number_seller_reviews_for_seller(seller_id)
    return render_template('sellerreviews.html',
                            sellerreviews = s_reviews,
                            sellerreviewstats = seller_review_stats,
                            SRcheck = SR_check,
                            sellername = seller_name,
                            number = number,
                            total = total_reviews)