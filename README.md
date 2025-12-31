# The Cricket Shop
#### Video Demo:  https://youtu.be/YC65at9FZus?si=zJZn6yYrhAY2jFDX
#### Description:
For the CS50 Final Project I developed an E-Commerce website using Flask, HTML, CSS and Javascript. It is about a local cricket shop and website can be used to make online purchases for your cricket equipment needs. It consits of 11 html pages, 1 app.py, 1 helpers.py, 1 shopping.db & 1 static folder consisting of script.js, stylesheet.css & images.

HTML templates

1. index.html: It is the homepage or the first page you will see on the launch of the webpage. It consists of navigation bar like all other pages that can be used to navigate to different section of the site. If you scroll down you will see the Welcome text & cricketer picture with a button "Explore Now" that will take you to the products section. Below that there is a shop by brands sections & can be used to filter products by brands.

2. about.html: As the name suggests this page consists of all the history & legacy of the store. Also what it stands for today, when it was founded & who it was founded by.

3. account.html: This is the login/ register page. There is a window that consists of Login/ Register tabs & can be used to switch between two. You must login before adding any products to the cart. After logging in it is replaced by logout.html

4. apology.html: This is an error token that is used to for client side validation. It consists of a grumpy cat & it displays the error message if you did not filled any required field.

5. cart.html: This is your shopping cart. Any products that you will add will appear here. You can see the name, image & the quantity of the item added. You can also remove the item(s). Below that there is a checkout button.

6. contact.html: This is the contact us page. Here it shows the phone, address, email & fax for the bussiness. Below that there is an embedded google map as well. After that there is a form that you can submit if you have any questions. Lastly there is a section that displays the store hours.

7. detail.html: This is the page that will open when you click any of the products displayed. It will go into detail for that product. It shows the description, various other images in a carousel & the quantity that you want to select. Also there is an "Add to Cart" button.

8. layout.html: This is the flask jinja layout page that extends all other pages. It consists of all the common things like navigation bar & footer. In the footer there are the links for the social medias as well the other sections of the site.

9. logout.html: When you first launch the app & open the account page, it displays account.html. After logging in it is replaced by this page, logout,\.hyml. It showed the signed in user with the button to logout.

10. products.html: This the products page. It consists of products 3 in a row & 3 rows in a page. There is also a navigation button at the bottom. When hovered over a product, It is highlighted & shadowed. There is option to add to cart or go the that product that will take you to the detail.html.

11. returns.html: Lastly the is Shipping & returns page that contain all the details about shipping services or how to start a return.

APP.py: This is the flask app page that connects all the html templates, the database & the queries.

shopping.db: This is the database used for this project. It consists of 5 tables:

I. users: It has 4 columns:
1. id: PRIMARY KEY
2. username
3. hash: Used to hash the password
4. name

II. sqlite_sequence:
1. name
2. seq

III. username: UNIQUE INDEX username ON users (username)

IV. brand: All the brands used in the webpage.
1. id: PRIMARY KEY
2. brand_name
3. brand_logo: aws images urls

V. products: It has 9 columns:

1. id: PRIMARY KEY
2. brand: It has 5 brands
3. product_title
4. name
5. price
6. decription
7. img1
8. img2
9. img3

img1, img2, & img3 are the aws bucket urls that contains the images used in detail.html carousel.

helpers.py: It has the implementation of apology that is it renders a template, apology.html. Also in the file is usd, a short function that simply formats a float as USD (e.g., 1234.56 is formatted as $1,234.56).

static folder: It contain 3 files:

1. images: All the images used in the web app.
2. myscript.js: Javascript used in the app.
3. styles.css: Stylesheet for the app.
