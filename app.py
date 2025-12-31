import os
import math
import sqlite3
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure sqlite3 Library to use SQLite database
con = sqlite3.connect("shopping.db", check_same_thread=False)
cur = con.cursor()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect("/account")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def default():
    cur.execute("SELECT * FROM brand")
    Logos = cur.fetchall()

    return render_template("index.html", Logos=Logos)

@app.route("/index")
def index():
    cur.execute("SELECT * FROM brand")
    Logos = cur.fetchall()

    return render_template("index.html", Logos=Logos)

@app.route("/products", methods=["GET", "POST"])
def products():
    per_page = 9
    current_page = int(request.args.get("page", 1))
    name = request.args.get('name')

    if name:
        cur.execute("SELECT COUNT(*) FROM products WHERE brand = ?;", [request.args.get('name')])
        total = cur.fetchone()[0]
        no_of_page = math.ceil(total/ per_page)

        offset = (current_page - 1) * per_page
        cur.execute("SELECT * FROM products WHERE brand = ? LIMIT ? OFFSET ?;", [request.args.get('name'), per_page, offset])
        products = cur.fetchall()

        return render_template("products.html", current_page=current_page, no_of_page=no_of_page, products=products, name=name)

    else:
        cur.execute("SELECT COUNT(*) FROM products")
        total = cur.fetchone()[0]
        no_of_page = math.ceil(total/ per_page)

        offset = (current_page - 1) * per_page
        cur.execute("SELECT * FROM products ORDER BY RANDOM() LIMIT ? OFFSET ?", [per_page, offset])
        products = cur.fetchall()

        return render_template("products.html", current_page=current_page, no_of_page=no_of_page, products=products)

@app.route("/detail", methods=["GET", "POST"])
def detail():
    cur.execute("SELECT * FROM products WHERE id = ?;", [request.args.get('name')])
    detail = cur.fetchall()
    return render_template("detail.html", detail=detail)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():

    if request.method == "POST":
        session.clear()
        return redirect("/account")

    else:
        return render_template("logout.html")

@app.route("/account",  methods=["GET", "POST"])
def account():

    if 'user_id' in session:
        return redirect("/logout")

    else:

        if request.method == "POST":

            # Form 1 : Login
            if request.form['btn'] == 'login':

                # Forget any user_id
                session.clear()
                username = request.form['username']
                password = request.form['password']

                if not username:
                    return apology("must provide username", 400)

                # Ensure password was submitted
                elif not password:
                    return apology("must provide password", 400)

                cur.execute("SELECT * FROM users WHERE username = ?;", [request.form['username']])
                con.commit()
                row = cur.fetchone()

                if not row:
                    return apology("Invalid Username!", 400)

                elif check_password_hash(row[2], password) != True:
                    return apology("Invalid Password!", 400)

                else:
                    session['user_id'] = row[0]
                    session['name'] = row[3]

                    return redirect("/")

            # Form 2 : Register
            elif request.form['btn'] == 'register':

                # Forget any user_id
                session.clear()
                cur.execute("SELECT * FROM users WHERE username = ?;", [request.form['registerUsername']])
                row = cur.fetchone()

                if not request.form['registerName']:
                    return apology("Must provide full name!", 400)

                elif not request.form['registerUsername']:
                    return apology("Must provide username!", 400)

                    # Ensure password was submitted
                elif not request.form['registerPassword']:
                    return apology("Must provide password!", 400)

                # Ensure confirmation was submitted
                elif not request.form['registerRepeatPassword']:
                    return apology("Must provide confirmation!", 400)

                # Ensure passwords match
                elif request.form['registerPassword'] != request.form['registerRepeatPassword']:
                    return apology("Password doesn't match", 400)

                elif row:
                    return apology("Username Exists! Please try a entering a different one", 400)

                else:
                    cur.execute("INSERT INTO users (username, hash, name) VALUES (?, ?, ?)",
                                    (request.form['registerUsername'], generate_password_hash(request.form['registerPassword']), request.form['registerName']))
                    con.commit()

                    # Once the form is executed redirect to login page
                    return redirect("/account")

        else:
            return render_template("account.html")


@app.route("/returns")
def returns():
    return render_template("returns.html")

@app.route("/add_to_cart", methods=["GET", "POST"])
def add_to_cart():

    if 'user_id' not in session:
        return redirect("/account")

    try:
        data = request.get_json(force=True)
    except:
        data = None

    if request.is_json:
        data = request.get_json()
        product_id = data['product_id']
        quantity = int(data.get('quantity', 1))

        cart = session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + quantity
        session['cart'] = cart

        total_items = sum(cart.values())

        return jsonify({'success': True, 'cart_count': total_items})

    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])

    cart = session.get('cart', {})

    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity

    session['cart'] = cart

    return redirect(url_for('detail', name=product_id))

@app.route("/cart")
@login_required
def cart():
    cart = session.get('cart', {})

    if not cart:
        return render_template("cart.html", cart=None)

    # Get product details from the database for each product ID in the cart
    items = []
    for product_id, quantity in cart.items():
        cur.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = cur.fetchone()
        items.append({
            'product': product,
            'quantity': quantity
        })

    # Calculate the total price for the cart (sum of all item totals)
    total_price = sum(item['quantity'] * item['product'][4] for item in items)

    return render_template("cart.html", items=items, total_price=total_price)

@app.route('/remove', methods=['GET', 'POST'])
def remove():
    product_id = request.args.get('name')

    cart = session.get('cart', {})
    cart.pop(product_id, None)
    session['cart'] = cart

    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    session.pop('cart', None)
    return redirect(url_for('cart'))
