from __future__ import print_function # In python 2.7
import sys
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_babel import _, lazy_gettext as _l


from .models.user import User
from .models.affirm import Affirm

from flask import Blueprint
bp = Blueprint('affirmations', __name__)

#form to add your own affirmation
class AffirmationForm(FlaskForm):
    affirmation = StringField(_l('Affirmation'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

#routes to all affirmation
@bp.route('/affirmations', methods=['GET', 'POST'])
def affirmations():
    #get profile info
    profile_info = User.get_profile(current_user.uid)
    affirmations = Affirm.get_affirmations()
    # render the page by adding information to the profile.html file
    return render_template('affirmations.html', profile = profile_info, all_affirmations = affirmations)

#routes to add affirmation form
@bp.route('/addaffirmation', methods=['GET', 'POST'])
def add():
    #form to add affirmation
    form = AffirmationForm()
    if form.validate_on_submit():
        Affirm.add_affirmation(form.affirmation.data)
        print('update worked')
        return redirect(url_for('affirmations.affirmations'))
    return render_template('addaffirmation.html', title='Add Affirmation', form=form)