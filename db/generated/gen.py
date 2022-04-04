from os import name
from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random

# num_users = 110
num_users = 500
num_products = 10000
num_purchases = 4000
num_sellers = 300
num_accounts = 400
num_categories = 20
num_carts = 1000
num_reviews = 20000

images = [
    "https://lh6.ggpht.com/HlgucZ0ylJAfZgusynnUwxNIgIp5htNhShF559x3dRXiuy_UdP3UQVLYW6c=s1200",
    "https://ih1.redbubble.net/image.482432505.2782/fposter,small,wall_texture,product,750x1000.jpg",
    "https://www.history.com/.image/ar_1:1%2Cc_fill%2Ccs_srgb%2Cfl_progressive%2Cq_auto:good%2Cw_1200/MTU3ODc4NTk4NjgxNjM0NTI3/hith-art-heists-scream-2.jpg",
    "https://art.art/wp-content/uploads/2021/09/fatcat_art.jpg",
    "https://pyxis.nymag.com/v1/imgs/a59/90b/ed419e06a1d46f317e4bb4f26c1f0ec78b-tshirt-ODE.rsquare.w1200.jpg",
    "https://m.media-amazon.com/images/I/71GxclaDNsL._AC_UX342_.jpg",
    "https://imgs.michaels.com/MAM/assets/1/726D45CA1C364650A39CD1B336F03305/img/91F89859AE004153A24E7852F8666F0F/10093625_r.jpg?fit=inside|540:540",
    "https://m.media-amazon.com/images/I/61fiCzz6rdL._AC_UY445_.jpg",
    "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/gray-sweats-1631821743.jpg?crop=1.00xw:1.00xh;0,0&resize=1200:*",
    "https://images.boardriders.com/global/billabong-products/all/default/hi-res/m302vbap_billabong,f_nvy_frt1.jpg",
    "https://m.media-amazon.com/images/I/61BsCX+8nIL._AC_UX385_.jpg",
    "https://m.media-amazon.com/images/I/51JISPYJlwL._AC_UX385_.jpg",
    "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6428/6428998_sd.jpg",
    "https://images.prismic.io/frameworkmarketplace/cca31de3-3b75-4932-af96-7646b7eba6c7__DSC3630-Edit-cropped.jpg?auto=compress,format",
    "https://i5.walmartimages.com/asr/ae9df631-3f57-4293-9c0c-be0f758e378a.bcd827b9231c9321f0d49a7d9b00121c.jpeg",
    "https://i5.walmartimages.com/asr/bb3c4eb0-0ada-4cef-8b5f-97a11fa7ef0f.2d3805e39285bde9b9884e68e76e3608.jpeg",
    "https://i.pinimg.com/474x/83/9a/08/839a0809148a30d5ac5a835dd90cb79f.jpg",
    "https://i.insider.com/5c799c56eb3ce834ad57b632?width=750&format=jpeg&auto=webp",
    "https://i.pinimg.com/originals/5b/b4/8b/5bb48b07fa6e3840bb3afa2bc821b882.jpg",
    "https://i.pinimg.com/736x/7a/15/52/7a155238ab97bf76ef1509f4a55242de.jpg",
    "https://www.simplyrecipes.com/thmb/8caxM88NgxZjz-T2aeRW3xjhzBg=/2000x1125/smart/filters:no_upscale()/__opt__aboutcom__coeus__resources__content_migration__simply_recipes__uploads__2019__09__easy-pepperoni-pizza-lead-3-8f256746d649404baa36a44d271329bc.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg",
    "https://www.glutenfreepalate.com/wp-content/uploads/2018/08/Gluten-Free-Pizza-3.2-480x360.jpg",
    "https://hips.hearstapps.com/hmg-prod/images/delish-bucatinipasta-028-ls-1607552701.jpg",
    "https://www.budgetbytes.com/wp-content/uploads/2013/07/Creamy-Spinach-Tomato-Pasta-bowl.jpg",
    "https://www.seriouseats.com/thmb/GSqpVkulyUZu-D6sPijmbFV_f4s=/1500x1125/filters:fill(auto,1)/__opt__aboutcom__coeus__resources__content_migration__serious_eats__seriouseats.com__2020__03__20200224-carretteira-pasta-vicky-wasik-21-ffe68515b25f4b348cbde845a59d6a62.jpg",
    "https://s23209.pcdn.co/wp-content/uploads/2013/10/IMG_4012edit1.jpg",
    "https://therecipecritic.com/wp-content/uploads/2019/07/easy_fried_rice-1-500x500.jpg",
    "https://images.japancentre.com/recipes/pics/18/main/makisushi.jpg?1557308201",
    "https://media.cntraveler.com/photos/603fc7a599ab9b035e060f47/7:10/w_1260,h_1800,c_limit/OutdoorBrands-EddieBauer-2021-1.jpg",
    "https://images.unsplash.com/photo-1543039625-14cbd3802e7d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8b3V0ZG9vcnxlbnwwfHwwfHw%3D&w=1000&q=80",
    "https://www.csun.edu/sites/default/files/AS-Earth_Month-Outdoor_Online.jpg",
    "https://www.roanoke.edu/images/campusrec/McAfee_Olivia.jpg",
    "https://images.squarespace-cdn.com/content/v1/5a5d344cb7411c8b282df032/1626121126360-VTU3UMXBLVKG0KJ1V4OK/unsplash-image-ITi2yqiwtBM.jpg?format=2500w",
    "https://www.rd.com/wp-content/uploads/2021/03/GettyImages-1133605325-scaled-e1617227898456.jpg",
    "https://www.akc.org/wp-content/uploads/2017/11/Labrador-Retriever-MP-500x486.jpg",
    "https://static.stacker.com/s3fs-public/2020-03/English%20Lab%20Puppy%20%281%29.png",
    "https://americanpetsalive.org/uploads/blog/Healthy-Kittens.jpg",
    "https://spca.bc.ca/wp-content/uploads/news-kittens.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/4/40/Heyward_lines_into_double_play_%2828356212176%29.jpg"
]

categories = [
    "art",
"books",
"clothing",
"drink",
"electronics",
"entertainment",
"food",
"home",
"outdoor",
"pets",
"sports",
"other",
]

Faker.seed(0)
fake = Faker()

def get_csv_writer(f):
    return csv.writer(f, dialect='unix')

#Users(uid, email, firstname, lastname, address, password)
def gen_users(num_users):
    with open('db/generated/Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            address = profile['residence']
            writer.writerow([uid, email, firstname, lastname, address, password])
        print(f'{num_users} generated')
    return

#Account(uid, balance)
def gen_account(num_accounts):
    with open('db/generated/Account.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Account...', end=' ', flush=True)
        for uid in range(num_accounts):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            balance = f'{str(fake.random_int(max=1000))}.{fake.random_int(max=99):02}'
            writer.writerow([uid, balance])
        print(f'{num_accounts} generated')
    return

#Purchases(oid, uid, time_purchased, total_amount, item_quantity, fulfillment_status, order_page)
def gen_purchases(num_purchases):
    with open('db/generated/Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for oid in range(num_purchases):
            if oid % 100 == 0:
                print(f'{oid}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            time_purchased = fake.date_time()
            total_amount = f'{str(fake.random_int(max=5000))}.{fake.random_int(max=99):02}'
            item_quantity = f'{str(fake.random_int(max=100))}'
            fulfillment_status = fake.random_element(elements=('Ordered', 'In Transit', 'Delivered'))
            order_page = fake.url()
            writer.writerow([oid, uid, time_purchased, total_amount, item_quantity, fulfillment_status, order_page])
        print(f'{num_purchases} generated')
    return

#Product_Categories(category)
def gen_product_categories(num_categories):
    with open('db/generated/Product_Categories.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Product Categories...', end=' ', flush=True)
        for categories in range(num_categories):
            if categories % 10 == 0:
                print(f'{categories}', end=' ', flush=True)
            category = fake.sentence(nb_words=2)[:-1]
            writer.writerow([category])
        print(f'{num_categories} generated')
    return

#Products(pid, name, price, available, img, description, category)
def gen_products(num_products):
    available_names = []
    available_pids = []
    available_prices = []
    with open('db/generated/Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            available_names.append(name)
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            available_prices.append(price)
            available = fake.random_element(elements=('true', 'false'))
            img = fake.random_element(images)
            description = fake.sentence(nb_words=15)[:-1]
            category = fake.random_element(categories)
            if available == 'true':
                available_pids.append(pid)
            writer.writerow([int(pid), name, price, available, img, description, category])
        print(f'{num_products} generated; {len(available_pids)} available')
    return (available_pids, available_names, available_prices)


# NEED TO FIX GENERATED DATA!!!
#Cart(uid, pid, p_quantity, unit_price, seller_id)
#Cart(cid)
def gen_cart(num_carts):
    with open('db/generated/Cart.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Cart...', end=' ', flush=True)
        for cid in range(num_carts):
            if cid % 10 == 0:
                print(f'{cid}', end=' ', flush=True)
            writer.writerow([cid])
        print(f'{num_carts} generated')
    return

#InCart(uid, pid, name, p_quantity, unit_price, seller_id)
def gen_in_cart(num_carts, names):
    with open('db/generated/InCart.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('In Cart...', end=' ', flush=True)
        for cid in range(num_carts):
            if cid % 100 == 0:
                print(f'{cid}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_int(min=0, max=num_products-1)
            # = fake.sentence(nb_words=4)[:-1]
            name = random.choice(names)
            p_quantity = f'{str(fake.random_int(min=1, max=100))}'
            unit_price = f'{str(fake.random_int(max=5000))}.{fake.random_int(max=99):02}'
            seller_id = fake.random_int(min=0, max=num_sellers-1)
            writer.writerow([uid, pid, name, p_quantity, unit_price, seller_id])
        print(f'{num_purchases} generated')
    return

#SaveForLater(uid, pid, name, p_quantity, unit_price, seller_id)
def gen_save_for_later(num_carts, num_products, available_name):
    with open('db/generated/SaveForLater.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Save For Later...', end=' ', flush=True)
        for cid in range(num_carts):
            if cid % 100 == 0:
                print(f'{cid}', end=' ', flush=True)
            pid = fake.random_int(min=0, max=num_products-1)
            uid = fake.random_int(min=0, max=num_users-1)
            p_quantity = f'{str(fake.random_int(min=1, max=100))}'
            unit_price = f'{str(fake.random_int(max=5000))}.{fake.random_int(max=99):02}'
            seller_id = fake.random_int(min=0, max=num_sellers-1)
            name = random.choice(available_name)
            writer.writerow([uid, pid, name, p_quantity, unit_price, seller_id])
        print(f'{num_purchases} generated')
    return


#Orders(cid, oid, order_totalPrice, fulfilled)
def gen_orders(num_purchases, num_carts):
    available_oid = []
    with open('db/generated/Orders.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Orders...', end=' ', flush=True)
        for oid in range(num_carts):
            if oid % 100 == 0:
                print(f'{oid}', end=' ', flush=True)
            # oid = fake.random_int(min=0, max=num_purchases-1)
            available_oid.append(oid)
            uid = fake.random_int(min=0, max=num_users-1)
            p_quantity = f'{str(fake.random_int(max=100))}'
            unit_price = f'{str(fake.random_int(max=5000))}.{fake.random_int(max=99):02}'
            available_prices.append(unit_price)
            order_totalPrice = str((int(p_quantity))*float(unit_price))
            fulfilled = fake.random_element(elements=('true', 'false'))
            time_purchased = fake.date_time()
            writer.writerow([oid, uid, order_totalPrice, fulfilled, time_purchased])
        print(f'{num_purchases} generated')
    return available_oid

#OrderedItems(uid, oid, pid, unit_price, p_quantity, fulfilled, fulfillment_time)
def gen_orderered_items(num_purchases, available_pids, available_prices, available_oids):
    with open('db/generated/OrderedItems.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Orderered Items...', end=' ', flush=True)
        for cid in range(num_carts):
            if cid % 100 == 0:
                print(f'{cid}', end=' ', flush=True)
            
            oid = random.choice(available_oids)
            uid = fake.random_int(min=0, max=num_users-1)
            idx = random.randrange(len(available_pids))
            pid = available_pids[idx]
            unit_price = available_prices[idx]
            p_quantity = f'{str(fake.random_int(max=100))}'
            unit_price = f'{str(fake.random_int(max=5000))}.{fake.random_int(max=99):02}'
            fulfilled = fake.random_element(elements=('true', 'false'))
            fulfillment_time = fake.date_time()
            writer.writerow([uid, oid, pid, unit_price, p_quantity, fulfilled, fulfillment_time])
        print(f'{num_purchases} generated')
    return

#Sellers(uid)
def gen_sellers(num_sellers):
    with open('db/generated/Sellers.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Sellers...', end=' ', flush=True)
        for uid in range(num_sellers):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            writer.writerow([uid])
        print(f'{num_sellers} generated')
    return


#Inventory(seller_id, pid, quantity)
def gen_inventory(num_products, available_pids):
    inventory = []
    with open('db/generated/Inventory.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Inventory...', end=' ', flush=True)
        for x in range(len(available_pids)):
            if x % 10 == 0:
                print(f'{x}', end=' ', flush=True)
            seller_id = f'{str(fake.random_int(max=num_sellers-1))}'
            pid = available_pids[x]
            if (seller_id, pid) not in inventory:
                inventory.append((seller_id, pid))
            else:
                seller_id = f'{str(fake.random_int(max=num_sellers-1))}'
            quantity = f'{str(fake.random_int(max=100))}'
            writer.writerow([seller_id, pid, quantity])
        print(f'{num_sellers} generated')
    return


#SellerOrders(seller_id, order_id, uid)
def gen_seller_orders(num_carts):
    with open('db/generated/SellerOrders.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Seller Orders...', end=' ', flush=True)
        for order_id in range(num_carts-1):
            if order_id % 10 == 0:
                print(f'{order_id}', end=' ', flush=True)
            seller_id = fake.random_int(max=num_sellers-1)
            uid = fake.random_int(max=num_users-1)
            writer.writerow([seller_id, order_id, uid])
        print(f'{num_carts} generated')
    return

#UpdateSubmission(buyer_balance, seller_balance, fulfilled_time, oid, cid, seller_id, total_price)
def gen_update_submission(num_purchases):
    with open('db/generated/UpdateSubmission.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Update Submission...', end=' ', flush=True)
        for oid in range(num_carts):
            if oid % 100 == 0:
                print(f'{oid}', end=' ', flush=True)
            cid = fake.random_int(min=0, max=num_purchases-1)
            seller_id = fake.random_int(min=0, max=num_sellers-1)
            #bid = fake.random_int(min=0, max=num_accounts-1) no table for this
            p_quantity = f'{str(fake.random_int(max=100))}'
            unit_price = f'{str(fake.random_int(max=5000))}.{fake.random_int(max=99):02}'
            total_price = str((int(p_quantity))*float(unit_price))
            fulfilled_time = fake.date_time()
            buyer_balance = f'{str(fake.random_int(max=5000))}.{fake.random_int(max=99):02}'
            seller_balance = f'{str(fake.random_int(max=5000))}.{fake.random_int(max=99):02}'
            writer.writerow([buyer_balance, seller_balance, fulfilled_time, oid, cid, seller_id, total_price])
        print(f'{num_purchases} generated')
    return


#Product_Reviews(uid, pid, time, rating, comments, votes)
def gen_product_reviews(num_products):
    combos = []
    with open('db/generated/Product_Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Product Reviews...', end=' ', flush=True)
        for x in range(num_reviews):
            if x % 10 == 0:
                print(f'{x}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_int(min=0, max=num_products-1)
            if (uid, pid) in combos:
                uid = uid + 1
            combos.append((uid,pid))
            time = fake.date_time()
            rating = fake.random_int(min=0, max=5)
            comments = fake.sentence(nb_words=20)[:-1]
            votes = fake.random_int(min=0, max=num_users-1)
            writer.writerow([uid, pid, time, rating, comments, votes])
        print(f'{num_categories} generated')
    return



#Seller_Reviews(uid, seller_id, time, rating, comments, votes)
def gen_seller_reviews(num_reviews):
    combos = []
    with open('db/generated/Seller_Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Seller Reviews...', end=' ', flush=True)
        for x in range(num_reviews-15000):
            if x % 10 == 0:
                print(f'{x}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            seller_id = fake.random_int(max=num_sellers-1)
            if (uid, seller_id) in combos:
                uid = fake.random_int(min=0, max=num_users-1)
                seller_id = fake.random_int(max=num_sellers-1)
            combos.append((uid, seller_id))
            time = fake.date_time()
            rating = fake.random_int(min=0, max=5)
            comments = fake.sentence(nb_words=20)[:-1]
            votes = fake.random_int(min=0, max=num_users-1)
            writer.writerow([uid, seller_id, time, rating, comments, votes])
        print(f'{num_categories} generated')
    return

#SR_Comments(rid, uid, seller_id, time_commented, comment, votes)
def gen_seller_comments(num_reviews):
    with open('db/generated/SR_Comments.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Seller Comments...', end=' ', flush=True)
        for uid in range(num_sellers):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            rid = fake.random_int(min=0, max=num_users-1)
            uid = fake.random_int(min=0, max=num_users-1)
            seller_id = fake.random_int(max=num_sellers-1)
            time = fake.date_time()
            comments = fake.sentence(nb_words=20)[:-1]
            votes = fake.random_int(min=0, max=num_users-1)
            writer.writerow([rid, uid, seller_id, time, comments, votes])
        print(f'{num_categories} generated')
    return

#PR_Comments(rid, uid, seller_id, time_commented, comment, votes)
def gen_product_comments(num_reviews):
    with open('db/generated/PR_Comments.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Product Comments...', end=' ', flush=True)
        for uid in range(num_sellers):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            rid = fake.random_int(min=0, max=num_users-1)
            uid = fake.random_int(min=0, max=num_users-1)
            seller_id = fake.random_int(max=num_sellers)
            time = fake.date_time()
            comments = fake.sentence(nb_words=20)[:-1]
            votes = fake.random_int(min=0, max=num_users-1)
            writer.writerow([rid, uid, seller_id, time, comments, votes])
        print(f'{num_categories} generated')
    return

#Images_Reviews(uid, pid, img)
def gen_images_reviews(num_products):
    with open('db/generated/Images_Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Images Reviews...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 10 == 0:
                print(f'{pid}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            img = fake.random_element(images)
            writer.writerow([uid, pid, img])
        print(f'{num_categories} generated')
    return


gen_users(num_users)
gen_account(num_accounts)
gen_purchases(num_purchases)

# gen_product_categories(num_categories)
available_pids, available_name, available_prices = gen_products(num_products)

#gen_cart(num_carts)
#gen_in_cart(num_carts, available_name)
#gen_save_for_later(num_carts, num_products, available_name)
available_oids = gen_orders(num_purchases, num_carts)
gen_orderered_items(num_purchases, available_pids, available_prices, available_oids)

gen_sellers(num_sellers)
gen_inventory(num_products, available_pids)
gen_seller_orders(num_carts)
gen_update_submission(num_purchases)

gen_product_reviews(num_products)
gen_seller_reviews(num_reviews)
gen_product_comments(num_products)
gen_seller_comments(num_sellers)
gen_images_reviews(num_products)