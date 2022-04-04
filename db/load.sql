\COPY Users FROM 'generated/Users.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.users_uid_seq',
                         (SELECT MAX(uid)+1 FROM Users),
                         false);
\COPY Product_Categories FROM 'generated/Product_Categories.csv' WITH DELIMITER ',' NULL '' CSV                         
\COPY Products FROM 'generated/Products.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Purchases FROM 'generated/Purchases.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Account FROM 'generated/Account.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Product_Reviews FROM 'generated/Product_Reviews.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Sellers FROM 'generated/Sellers.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Inventory FROM 'generated/Inventory.csv' WITH DELIMITER ',' NULL '' CSV
\COPY InCart FROM 'generated/InCart.csv' WITH DELIMITER ',' NULL '' CSV
\COPY SaveForLater FROM 'generated/SaveForLater.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Orders FROM 'generated/Orders.csv' WITH DELIMITER ',' NULL '' CSV
\COPY OrderedItems FROM 'generated/OrderedItems.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Seller_Reviews FROM 'generated/Seller_Reviews.csv' WITH DELIMITER ',' NULL '' CSV
\COPY SellerOrders FROM 'generated/SellerOrders.csv' WITH DELIMITER ',' NULL '' CSV
\COPY PR_Comments FROM 'generated/PR_Comments.csv' WITH DELIMITER ',' NULL '' CSV
\COPY SR_Comments FROM 'generated/SR_Comments.csv' WITH DELIMITER ',' NULL '' CSV
