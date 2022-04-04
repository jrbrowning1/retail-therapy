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
bp = Blueprint('pastOrderspage', __name__)

#gets the page of all past orders
@bp.route('/pastOrderspage', methods=['GET', 'POST'])
def pastOrderspage():
    orders = pastOrders.get_orders(current_user.uid)
    pastOrders.get_status(current_user.uid, orders)
    orders = pastOrders.get_orders(current_user.uid)
    return render_template('pastOrders.html', orders = orders)#, status = status)