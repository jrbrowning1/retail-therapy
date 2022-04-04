from flask import render_template
from flask_login import current_user
import datetime

from .models.cart import Cart
from .models.saveforlater import Later

from flask import Blueprint
bp = Blueprint('saveforlaterPage', __name__)

#gets the save for later page
@bp.route('/saveforlaterPage')
def saveforlaterPage():
    cart_items = Later.get_cart(current_user.uid)
    return render_template('SaveForLater.html', items=cart_items)

#adding item to save for later and deleting from cart
@bp.route('/add_Cart/<int:pid>/<int:uid>', methods=['GET', 'POST'])
def add_Cart(pid, uid):
    print("we are here")
    In = Later.check(pid, uid)

    if (In is True):
        print("It is in cart")

        message = '[Already in Save for Later]'
        cart_items = Cart.get_cart(uid)
        cart_total = Cart.get_total(uid)
        return render_template(('cart.html'), message = message, items=cart_items, total = cart_total)
    else: 
        print("not in cart")
        Later.add(pid, uid)
        Cart.remove(pid, uid)
        cart_items = Cart.get_cart(uid)
        cart_total = Cart.get_total(uid)
        return render_template(('cart.html'), items=cart_items, total = cart_total)

#removing item from save for later and adding back to cart
@bp.route('/remove_product/<int:pid>/<int:uid>', methods=['GET', 'POST'])
def remove_product(pid, uid):
    Later.remove(pid, current_user.uid)
    print("removed item")
    In = Cart.check(pid, current_user.uid)
    if (In is True):
        print("It is in cart")
        Cart.update(pid, current_user.uid, 'add')
    else: 
        print("not in cart")
        Cart.add(pid, uid)
    cart_items = Later.get_cart(current_user.uid)
    return render_template('SaveForLater.html', items=cart_items)






