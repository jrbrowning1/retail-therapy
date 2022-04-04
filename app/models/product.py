from __future__ import print_function # In python 2.7
from flask import current_app as app
from sqlalchemy import text

import sys

import sqlalchemy

# product class
class Product:
    def __init__(self, pid, name, price, available, image, description, category):
        self.pid = pid
        self.name = name
        self.price = price
        self.available = available
        self.image = image
        self.description = description
        self.category = category

    # get product info using product id
    @staticmethod
    def get(pid):
        rows = app.db.execute('''
SELECT pid, name, price, available, image, description, category
FROM Products
WHERE pid = :pid
''',
                              pid=pid)
        return Product(*(rows[0])) if rows is not None else None

    # get all available products
    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT pid, name, price, available, image, description, category
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]

    # get all top rated and most reviewed products
    @staticmethod
    def get_top(available=True):
        rows = app.db.execute('''
SELECT pid, name, price, available, image, description, category
FROM (
WITH prod_rating  AS (
SELECT pid, AVG(rating)::numeric(10,2) AS avg, COUNT(pid) AS count
FROM Product_Reviews
GROUP BY pid)
SELECT Products.pid, name, price, available, image, description, category, prod_stats.avg AS rating, prod_stats.count AS count
FROM Products
RIGHT JOIN
(SELECT pid, avg, count 
FROM prod_rating
WHERE count > 0) AS prod_stats
ON prod_stats.pid = Products.pid
WHERE available = :available
ORDER BY rating DESC, count DESC
LIMIT 12 ) AS foo
''',
                              available=available)
        return [Product(*row) for row in rows]

    # get name of product using product id
    @staticmethod
    def get_name(pid):
        rows = app.db.execute('''
SELECT pid, name, image
FROM Products
WHERE pid = :pid
''',
                            pid=pid)
        return (rows[0]) if rows else None

    # get the different categories that products may belong to
    @staticmethod
    def get_categories():
        rows = app.db.execute('''
SELECT DISTINCT category FROM products      
''')
        return [(row[0]) for row in rows] if rows else None

    # get products using category search
    @staticmethod
    def get_prod_by_cat(category, sortCriteria, filterCriteria, number):
        
        # default descriptions for sorting and filtering
        sorting_descrip = '(SELECT NULL)'
        filtering_descrip = ''

        # all possible types of sorting
        if (sortCriteria == 'high'):
            sorting_descrip = '''price DESC'''
        if (sortCriteria == 'low'):
            sorting_descrip = '''price ASC'''
        if (sortCriteria == 'high_rating'):
            sorting_descrip = '''rating DESC NULLS LAST'''
        if (sortCriteria == 'low_rating'):
            sorting_descrip = '''rating ASC NULLS LAST'''
        
        # filtering by price
        if (filterCriteria == 'under25'):
            filtering_descrip = '''AND Products.price >= 0 AND Products.price < 25'''
        if (filterCriteria == '25to50'):
            filtering_descrip = '''AND Products.price >= 25 AND Products.price < 50'''
        if (filterCriteria == '50to100'):
            filtering_descrip = '''AND Products.price >= 50 AND Products.price < 100'''
        if (filterCriteria == '100to200'):
            filtering_descrip = '''AND Products.price >= 100 AND Products.price < 200'''
        if (filterCriteria == '200&Up'):
            filtering_descrip = '''AND Products.price >= 200'''

        # filtering by rating
        if (filterCriteria == '1&Up'):
            filtering_descrip = '''AND prod_rating.avg >= 1'''
        if (filterCriteria == '2&Up'):
            filtering_descrip = '''AND prod_rating.avg >= 2'''
        if (filterCriteria == '3&Up'):
            filtering_descrip = '''AND prod_rating.avg >= 3'''
        if (filterCriteria == '4&Up'):
            filtering_descrip = '''AND prod_rating.avg >= 4'''

        # not vulnerable to SQL inject attacks because I control the values being inserted into the query, not the user
        rows = app.db.execute('''
WITH prod_rating  AS (
SELECT pid, AVG(rating)::numeric(10,2) AS avg
FROM Product_Reviews
GROUP BY pid)
SELECT Products.pid, Products.name, Products.price, Products.available, Products.image, prod_rating.avg AS rating
FROM Products
FULL OUTER JOIN
prod_rating
ON prod_rating.pid = Products.pid
WHERE Products.category = :category
''' + filtering_descrip + 
'''ORDER BY ''' + sorting_descrip + 
''' LIMIT 9
OFFSET :number
''', 
category=category, number=number)
        return rows if rows else None

    # get products using keyword search
    @staticmethod
    def get_by_keyword(words, sortCriteria, filterCriteria, number):
        
        # default descriptions for sorting and filtering
        sorting_descrip = '(SELECT NULL)'
        filtering_descrip = ''

        if (sortCriteria == 'high'):
            sorting_descrip = '''price DESC'''
        if (sortCriteria == 'low'):
            sorting_descrip = '''price ASC'''
        if (sortCriteria == 'high_rating'):
            sorting_descrip = '''rating DESC NULLS LAST'''
        if (sortCriteria == 'low_rating'):
            sorting_descrip = '''rating ASC NULLS LAST'''

        # filtering by price
        if (filterCriteria == 'under25'):
            filtering_descrip = '''AND (Products.price >= 0 AND Products.price < 25)'''
        if (filterCriteria == '25to50'):
            filtering_descrip = '''AND (Products.price >= 25 AND Products.price < 50)'''
        if (filterCriteria == '50to100'):
            filtering_descrip = '''AND (Products.price >= 50 AND Products.price < 100)'''
        if (filterCriteria == '100to200'):
            filtering_descrip = '''AND (Products.price >= 100 AND Products.price < 200)'''
        if (filterCriteria == '200&Up'):
            filtering_descrip = '''AND Products.price >= 200'''
        
        # filtering by rating
        if (filterCriteria == '1&Up'):
            filtering_descrip = '''AND prod_rating.avg >= 1'''
        if (filterCriteria == '2&Up'):
            filtering_descrip = '''AND prod_rating.avg >= 2'''
        if (filterCriteria == '3&Up'):
            filtering_descrip = '''AND prod_rating.avg >= 3'''
        if (filterCriteria == '4&Up'):
            filtering_descrip = '''AND prod_rating.avg >= 4'''

        # not vulnerable to SQL inject attacks because I control the values being inserted into the query, not the user
        rows = app.db.execute('''
WITH prod_rating  AS (
SELECT pid, AVG(rating)::numeric(10,2) AS avg
FROM Product_Reviews
GROUP BY pid)
SELECT Products.pid, Products.name, Products.available, Products.price, Products.image, prod_rating.avg AS rating
FROM Products
FULL OUTER JOIN
prod_rating
ON prod_rating.pid = Products.pid
WHERE (name LIKE ANY (:words)
OR description LIKE ANY (:words)
) ''' + filtering_descrip + 
'''ORDER BY ''' + sorting_descrip +
''' LIMIT 9
OFFSET :number
''',    
words = words, number=number)
        return rows if rows else None

    # get total number of products for category search
    @staticmethod
    def get_total_prod_by_cat(category, sortCriteria, filterCriteria):
        
        # default descriptions for sorting and filtering
        sorting_descrip = '(SELECT NULL)'
        filtering_descrip = ''

        # all possible types of sorting
        if (sortCriteria == 'high'):
            sorting_descrip = '''price DESC'''
        if (sortCriteria == 'low'):
            sorting_descrip = '''price ASC'''
        if (sortCriteria == 'high_rating'):
            sorting_descrip = '''rating DESC NULLS LAST'''
        if (sortCriteria == 'low_rating'):
            sorting_descrip = '''rating ASC NULLS LAST'''
        
        # filtering by price
        if (filterCriteria == 'under25'):
            filtering_descrip = '''AND Products.price >= 0 AND Products.price < 25'''
        if (filterCriteria == '25to50'):
            filtering_descrip = '''AND Products.price >= 25 AND Products.price < 50'''
        if (filterCriteria == '50to100'):
            filtering_descrip = '''AND Products.price >= 50 AND Products.price < 100'''
        if (filterCriteria == '100to200'):
            filtering_descrip = '''AND Products.price >= 100 AND Products.price < 200'''
        if (filterCriteria == '200&Up'):
            filtering_descrip = '''AND Products.price >= 200'''

        # filtering by rating
        if (filterCriteria == '1&Up'):
            filtering_descrip = '''AND prod_rating.avg >= 1'''
        if (filterCriteria == '2&Up'):
            filtering_descrip = '''AND prod_rating.avg >= 2'''
        if (filterCriteria == '3&Up'):
            filtering_descrip = '''AND prod_rating.avg >= 3'''
        if (filterCriteria == '4&Up'):
            filtering_descrip = '''AND prod_rating.avg >= 4'''
        
        # not vulnerable to SQL inject attacks because I control the values being inserted into the query, not the user
        rows = app.db.execute('''
SELECT Products.pid, Products.name, Products.price, Products.image
FROM Products
WHERE Products.category = :category
''' + filtering_descrip + 
'''ORDER BY ''' + sorting_descrip, 
category=category)
        return len(rows)

    # get total number of products for keyword search
    @staticmethod
    def get_total_by_keyword(words, sortCriteria, filterCriteria):

        # default descriptions for sorting and filtering
        sorting_descrip = '(SELECT NULL)'
        filtering_descrip = ''

        # all possible types of sorting
        if (sortCriteria == 'high'):
            sorting_descrip = '''price DESC'''
        if (sortCriteria == 'low'):
            sorting_descrip = '''price ASC'''
        if (sortCriteria == 'high_rating'):
            sorting_descrip = '''rating DESC NULLS LAST'''
        if (sortCriteria == 'low_rating'):
            sorting_descrip = '''rating ASC NULLS LAST'''

        # filtering by price
        if (filterCriteria == 'under25'):
            filtering_descrip = '''AND (Products.price >= 0 AND Products.price < 25)'''
        if (filterCriteria == '25to50'):
            filtering_descrip = '''AND (Products.price >= 25 AND Products.price < 50)'''
        if (filterCriteria == '50to100'):
            filtering_descrip = '''AND (Products.price >= 50 AND Products.price < 100)'''
        if (filterCriteria == '100to200'):
            filtering_descrip = '''AND (Products.price >= 100 AND Products.price < 200)'''
        if (filterCriteria == '200&Up'):
            filtering_descrip = '''AND Products.price >= 200'''
        
        # filtering by rating
        if (filterCriteria == '1&Up'):
            filtering_descrip = '''AND prod_rating.avg >= 1'''
        if (filterCriteria == '2&Up'):
            filtering_descrip = '''AND prod_rating.avg >= 2'''
        if (filterCriteria == '3&Up'):
            filtering_descrip = '''AND prod_rating.avg >= 3'''
        if (filterCriteria == '4&Up'):
            filtering_descrip = '''AND prod_rating.avg >= 4'''
        
        # not vulnerable to SQL inject attacks because I control the values being inserted into the query, not the user
        rows = app.db.execute('''
SELECT Products.pid, Products.name, Products.price, Products.image
FROM Products
WHERE (name LIKE ANY (:words)
OR description LIKE ANY (:words)
) ''' + filtering_descrip + 
'''ORDER BY ''' + sorting_descrip,    
words = words)
        return len(rows)


    # get all available products
    @staticmethod
    def get_sellers(pid):
        rows = app.db.execute('''
SELECT seller_id, in_stock
FROM Inventory
WHERE pid = :pid
''',
                              pid = pid)
        return rows if rows else None