from __future__ import print_function # In python 2.7
from flask import render_template
from flask_login import current_user
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import null, true

#import models
from .models.product import Product

from flask import Blueprint

import sys
bp = Blueprint('prodsearch', __name__)

# executes product search by category
@bp.route('/prodsearch/<category>/<int:number>', methods=['GET', 'POST'])
def ProductSearch(category, number):
    # print('this is the product category we are searching for', file=sys.stderr)
    # print(category, file=sys.stderr)
    
    # get products by category by calling SQL backend
    products = Product.get_prod_by_cat(category, number = number, sortCriteria='high', filterCriteria='none')
    
    # get total number of products for this search (needed for pagination)
    total_num_prod = Product.get_total_prod_by_cat(category, sortCriteria='high', filterCriteria='none')
    
    # print('this is total num prod in cat ', file=sys.stderr)
    # print(total_num_prod, file=sys.stderr)
    # print(products, file=sys.stderr)
    
    # return template and pertinent variables
    return render_template('prod-search.html',
                            category = category,
                            products = products, 
                            category_search = 'true',
                            sort_criteria = 'none',
                            filter_criteria = 'none',
                            number = number,
                            total = total_num_prod)

#executes product search by keyword
@bp.route('/keywordsearch/<keywords>/<int:number>', methods=['GET', 'POST'])
def ProductKeywordSearch(keywords, number):
    keywords_original = keywords
    
    # turn given keywords into list
    keywords = keywords.strip()
    keywords = list(keywords.split(" "))

    # adjust keywords so that SQL can handle them
    keywords_adj = []
    for word in keywords:
        temp_word = '%' + word + '%'
        # print(temp_word, file=sys.stderr)
        keywords_adj.append(temp_word)

    # get products by keyword
    products = Product.get_by_keyword(keywords_adj, number=number, sortCriteria='low', filterCriteria='none')

    # get total number of products for this search (needed for pagination)
    total_num_prod = Product.get_total_by_keyword(keywords_adj, sortCriteria='low', filterCriteria='none')
    
    # print('this is total num prod with key ', file=sys.stderr)
    # print(total_num_prod, file=sys.stderr)
    
    # return template and pertinent variables
    return render_template('prod-search.html',
                            category = keywords_original,
                            products = products, 
                            category_search = 'false',
                            sort_criteria = 'none',
                            filter_criteria = 'none',
                            number = number,
                            total = total_num_prod)

#executes sorting of search
@bp.route('/search/<keywords>/sort/<sortCriteria>/filter/<filterCriteria>/categorySearch/<category_search>/<int:number>', methods=['GET', 'POST'])
def FilterSort(keywords, sortCriteria, filterCriteria, category_search, number):
    # if the original search was a category search
    if (category_search == 'true'):
        # get products and total number of products
        products = Product.get_prod_by_cat(keywords, sortCriteria, filterCriteria, number)
        total_num_prod = Product.get_total_prod_by_cat(keywords, sortCriteria='high', filterCriteria='none')

    # if the original search was a keyword search
    else:
        # clean up keyword list again
        keywords_arr = keywords.strip()
        keywords_arr = list(keywords.split(" "))
        keywords_adj = []
        
        # adjust keywords so that SQL can use them
        for word in keywords_arr:
            temp_word = '%' + word + '%'
            keywords_adj.append(temp_word)
        
        # get products and total number of products
        products = Product.get_by_keyword(keywords_adj, sortCriteria, filterCriteria, number)
        total_num_prod = Product.get_total_by_keyword(keywords_adj, sortCriteria='low', filterCriteria='none')
    
    # print("the filter criteria is " + filterCriteria, file=sys.stderr)
    
    # if there isn't a filter criteria, change it to none to prevent URL errors
    if (filterCriteria == ''):
        # print('filtering shuild be changed now ', file=sys.stderr)
        filterCriteria = 'none'
    
    # if there isn't a sort criteria, change it to none to prevent URL errors
    if (sortCriteria == ''):
        # print('sorting shuild be changed now ', file=sys.stderr)
        sortCriteria = 'none'

    # return template and pertinent variables
    return render_template('prod-search.html',
                            category = keywords,
                            products = products,
                            category_search = category_search,
                            sort_criteria = sortCriteria,
                            filter_criteria = filterCriteria,
                            number = number,
                            total = total_num_prod)
