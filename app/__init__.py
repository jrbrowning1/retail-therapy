from flask import Flask
from flask_login import LoginManager
from flask_babel import Babel
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'
babel = Babel()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)
    babel.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .ProductReviews import bp as review_bp
    app.register_blueprint(review_bp)

    from .OneProduct import bp as product_bp
    app.register_blueprint(product_bp)

    from .cart import bp as cart_bp
    app.register_blueprint(cart_bp)

    from .ProductSearch import bp as search_bp
    app.register_blueprint(search_bp)

    from .profile import bp as profile_bp
    app.register_blueprint(profile_bp)

    from .PRComments import bp as prcomment_bp
    app.register_blueprint(prcomment_bp)

    from .sellers import bp as sellers_bp
    app.register_blueprint(sellers_bp)

    from .seller import bp as seller_bp
    app.register_blueprint(seller_bp)

    from .AddProductReviews import bp as addpr_bp
    app.register_blueprint(addpr_bp)

    from .AddPReviewComments import bp as addprc_bp
    app.register_blueprint(addprc_bp)

    from .orderPage import bp as op_bp
    app.register_blueprint(op_bp)

    from .SellerReviews import bp as sellerreview_bp
    app.register_blueprint(sellerreview_bp)
    
    from .AddSellerReviews import bp as addsr_bp
    app.register_blueprint(addsr_bp)

    from .SRComments import bp as srcomment_bp
    app.register_blueprint(srcomment_bp)

    from .AddSReviewComments import bp as addsrc_bp
    app.register_blueprint(addsrc_bp)

    from .pastOrderspage import bp as pop_bp
    app.register_blueprint(pop_bp)

    from .affirmations import bp as affirm_bp
    app.register_blueprint(affirm_bp)

    from .ind_orderPage import bp as iop_bp
    app.register_blueprint(iop_bp)
    
    from .saveforlaterPage import bp as sfl_bp
    app.register_blueprint(sfl_bp)

    return app
