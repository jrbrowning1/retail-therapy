from __future__ import print_function # In python 2.7
import sys
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.user import User
from .models.product import Product
from .models.cart import Cart
from .models.order_checkout import Order
from .models.pastOrders import pastOrders
import datetime
 
from flask import Blueprint
bp = Blueprint('ind_orderPage', __name__)


@bp.route('/ind_orderPage/<int:oid>', methods=['GET', 'POST'])
def ind_orderPage(oid):
    #print('got ind order')
    items = pastOrders.get_orderedProducts(current_user.uid, oid)
    #print(items)
    #print(item.name for item in items)
    return render_template('ind_orderpage.html', items=items)