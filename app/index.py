from __future__ import print_function # In python 2.7
from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.user import User

from flask import Blueprint
import sys
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # get all available products for sale:
    #products = Product.get_all(True)
    products = Product.get_top(True)
    # find the products current user has bought:
    # TO FIX: PURCHASES IS CURRENTLY BROKEN
    # if current_user.is_authenticated:
    #     purchases = Purchase.get_all_by_uid_since(
    #         current_user.uid, datetime.datetime(1980, 9, 14, 0, 0, 0))
    # else:
    purchases = None
    categories = Product.get_categories()
    print("these are the categories", file=sys.stderr)
    print(categories, file=sys.stderr)
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases,
                           categories=categories)


 