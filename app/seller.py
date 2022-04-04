from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.user import User
from .models.seller import Seller
from .models.sellerreview import SellerReview

from flask import Blueprint
bp = Blueprint('seller', __name__)

@bp.route('/seller/<int:uid>')
def seller(uid):
    products = Seller.get_seller_products(uid)
    seller = Seller.get_seller_info(uid)
    SR_check = True
    if current_user.is_authenticated:
        SR_check = SellerReview.review_check(uid, current_user.uid)
    return render_template('sellerpublic.html', slr=seller, inv=products, SRcheck = SR_check)