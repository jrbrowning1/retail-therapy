from __future__ import print_function # In python 2.7
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_babel import _, lazy_gettext as _l


from .models.user import User
from .models.seller import Seller
from .models.account import Account
from .models.productreview import ProductReview
from .models.sellerreview import SellerReview
from .models.pastOrders import pastOrders

from flask import Blueprint
bp = Blueprint('profile', __name__)

#routes to profile page
@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    #get profile info
    profile_info = User.get_profile(current_user.uid)
    new_balance = round(Account.get_balance(current_user.uid), 2)
    product_reviews = ProductReview.get_all_product_reviews_by_user(current_user.uid)
    seller_reviews = SellerReview.get_all_seller_reviews_by_user(current_user.uid)
    all_orders = pastOrders.get_orders(current_user.uid)
    # render the page by adding information to the profile.html file
    return render_template('profile.html', current_user = profile_info, 
                                            current_balance = new_balance,
                                            productreviews = product_reviews,
                                            sellerreviews = seller_reviews,
                                            orders = all_orders)

#routes to public profile page
@bp.route('/profile/public', methods=['GET', 'POST'])
def public():
    #get public info
    public_info = User.get_public(current_user.uid)
    public_seller = User.get_public_seller(current_user.uid)
    # render the page by adding information to the public.html file
    return render_template('public.html', public_user = public_info, public_seller = public_seller)

#routes to seller page
@bp.route('/seller')
def seller():
    User.make_seller(current_user.uid)
    products = Seller.get_seller_products(current_user.uid)
    seller = Seller.get_seller_info(current_user.uid)
    orders = sorted(Seller.get_seller_orders(current_user.uid), key=lambda x: x[3], reverse=True) # sort in reverse chronological order
    return render_template('seller.html', slr=seller, inv=products, ords=orders)

@bp.route('/seller/sort<sort_category>')
def sellersorted(sort_category=0):
    # seller page with the inventory sorted. sort_category specifies on what criteria the inventory should be sorted
    User.make_seller(current_user.uid)
    products = Seller.get_seller_products(current_user.uid)
    products = sorted(products, key=lambda x: x[int(sort_category)])
    seller = Seller.get_seller_info(current_user.uid)
    orders = sorted(Seller.get_seller_orders(current_user.uid), key=lambda x: x[3], reverse=True) # sort in reverse chronological order
    return render_template('seller.html', slr=seller, inv=products, ords=orders)

@bp.route('/seller/additem', methods=['GET', 'POST'])
def additem():
    form = AddToInventoryForm()
    form.category.choices = Seller.get_choices() # these are the choices for the category dropdown menu
    if form.validate_on_submit():
        if Seller.add_to_inventory(form.productname.data, form.price.data, form.quantity.data, form.description.data, form.image.data, form.category.data):
            return redirect(url_for('profile.seller'))
    return render_template('additem.html', title='Add item', form=form)

class AddToInventoryForm(FlaskForm):
    # form that a seller can use to add an item to inventory
    productname = StringField(_l('Product Name'), validators=[DataRequired()])
    price = DecimalField(_l('Price'), validators=[DataRequired()])
    quantity = IntegerField(_l('Quantity Available'), validators=[NumberRange(min=0)])
    description = StringField(_l('Description (max 2048 characters)'), validators=[DataRequired()])
    image = StringField(_l('Image URL'), validators=[DataRequired()])
    category = SelectField(u'Category', validators=[DataRequired()])
    submit = SubmitField(_l('Add to Inventory'))   

@bp.route('/seller/edititem-<pid>-<pname>-<price>-<stock>', methods=['GET', 'POST'])
def edititem(pid, pname, price, stock):
    form = EditInventoryForm()
    form.productname.data = pname       # \
    form.price.data = float(price)      #  } these lines are for autofilling the form with the old item's info
    form.quantity.data = int(stock)     # /
    form.category.choices = Seller.get_choices()
    if form.validate_on_submit():
        if Seller.edit_in_inventory(pid, form.productname.data, form.price.data, form.quantity.data, form.description.data, form.image.data, form.category.data):
            return redirect(url_for('profile.seller'))
    return render_template('edititem.html', title='Edit item', form=form, pid=pid)

class EditInventoryForm(FlaskForm):
    # form that a seller can use to edit an item in inventory
    productname = StringField(_l('Product Name'), validators=[DataRequired()])
    price = DecimalField(_l('Price'), validators=[DataRequired()])
    quantity = IntegerField(_l('Quantity Available'), validators=[NumberRange(min=0)])
    description = StringField(_l('Description (max 2048 characters)'), validators=[DataRequired()])
    image = StringField(_l('Image URL'), validators=[DataRequired()])
    category = SelectField(u'Category', validators=[DataRequired()])
    submit = SubmitField(_l('Save Changes'))

@bp.route('/seller/deleteitem-<pid>-<pname>', methods=['GET', 'POST'])
def deleteitem(pid, pname):
    # page on which a seller confirms they want to delete an item
    return render_template('deleteitem.html', pid=pid, pname=pname)

@bp.route('/seller/deleteditem-<pid>')
def deleteditem(pid):
    # page that confirms an item has been deleted
    Seller.delete_from_inventory(pid)
    return render_template('deleteditem.html')

@bp.route('/seller/fulfillitem-<oid>-<pid>')
def fulfillitem(oid, pid):
    # page that confirms a portion of an order has been fulfilled
    Seller.mark_item_fulfilled(oid, pid)
    return render_template('fulfilleditem.html', oid=oid, pid=pid)
