from flask import render_template
from flask_login import current_user
import datetime

from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('cart', __name__)


#cart page 
@bp.route('/cart')
def cart():
    cart_items = Cart.get_cart(current_user.uid)
    cart_total = Cart.get_total(current_user.uid)
    return render_template('cart.html', items=cart_items, total = cart_total)




