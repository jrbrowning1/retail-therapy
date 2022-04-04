from __future__ import print_function # In python 2.7
from flask import render_template
from flask_login import current_user

from app.models.productreview import ProductReview

#import models
from .models.product import Product
from .models.productreview import ProductReview

from flask import Blueprint

import sys
bp = Blueprint('oneproduct', __name__)

# routes to individual product page
@bp.route('/oneproduct/<int:product_number>', methods=['GET', 'POST'])
def OneProducts(product_number):
    # print("this is the product number", product_number, file=sys.stderr)
    # print(product_number, file=sys.stderr)
    
    # get product info and product rating
    p_info = Product.get(product_number)
    p_rating = ProductReview.get_just_rating(product_number)
    
    # print("this is the product rating ", file=sys.stderr)
    # print(p_rating, file=sys.stderr)
    # print(p_info, file=sys.stderr)
    
    PR_check = True
    
    # check to see if user has already given product a review
    if current_user.is_authenticated:
        PR_check = ProductReview.review_check(product_number, current_user.uid)
    
    sellers = Product.get_sellers(product_number)
    # return template and pertinent variables
    return render_template('ind-product-page.html',
                            productinfo = p_info,
                            product_rating = p_rating,
                            productreviewcheck = PR_check,
                            sellers = sellers)       