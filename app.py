import os
import psycopg2
import bcrypt
from flask import Flask, request, redirect, render_template, session


# get DATABASE_URL value from environment,
# if the value is NOT found, then use 'dbname=food_truck'
DATABASE_URL = os.environ.get('DATABASE_URL', 'dbname=tc_store')

# get SECRET_KEY value from environment,
# if the value is NOT found, then use 'bambi-thumper-example'
#
# Tip:
# 
# You can use the following code snippet to generate random secret key for your production environment
#   import secrets
#   secrets.token_hex(16)
SECRET_KEY = os.environ.get('SECRET_KEY', 'bambi-thumper-example')

app = Flask (__name__)
app.secret_key = SECRET_KEY.encode()

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/collection')
def collection():
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id, name, image_url_1, image_url_2, qty, price
        FROM toy
        LIMIT 100
    """)
    result = cursor.fetchall()
    
    toy_collection = result

    # using the cookie given to us by the browser
    # look up username in our DB
    user_id_from_encrypted_cookie = session.get("user_id")
    if user_id_from_encrypted_cookie:
        cursor.execute("""
            SELECT username
            FROM users
            WHERE id = %s
            LIMIT 1
        """, (user_id_from_encrypted_cookie,))
        result = cursor.fetchone()
    else:
        result = None
    if result:
        username = result
    else:
        username = None

    return render_template("collection.html", toy=toy_collection, username=username)

@app.route('/add_cart', methods=['post'])
def add_cart():
    toy_id = request.form.get('id')
    # TODO: Add a login page so that we have user id in the session
    user_id = '1'

    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()

    cursor.execute('SELECT quantity FROM CART WHERE user_id=%s and toy_id=%s', [user_id, toy_id])
    existingCartItem = cursor.fetchall()

    if len(existingCartItem) == 0:
        cursor.execute('INSERT INTO cart(user_id, toy_id, quantity) VALUES(%s, %s, 1)', [user_id, toy_id])
    else:
        cursor.execute('UPDATE cart SET quantity = %s WHERE  user_id=%s and toy_id=%s', [existingCartItem[0][0] + 1, user_id, toy_id])

    connection.commit()

    return redirect(request.referrer)

@app.route('/cart', methods=['GET'])
def cart():
    name = request.form.get('name')
    user_id = '1'
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute('SELECT toy.id, toy.name, quantity, image_url_1, price FROM cart, toy WHERE cart.user_id = %s AND cart.toy_id = toy.id', [user_id])
    cart = cursor.fetchall()
    return render_template("cart.html", cart=cart)


@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route("/login")
def login_page():
    # plumbing code for us to query DB
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()

    # using the cookie given to us by the browser
    # look up username in our DB
    user_id_from_encrypted_cookie = session.get("user_id")
    if user_id_from_encrypted_cookie:
        cursor.execute("""
            SELECT username
            FROM users
            WHERE id = %s
            LIMIT 1
        """, (user_id_from_encrypted_cookie,))
        result = cursor.fetchone()
    else:
        result = None
    if result:
        username, = result
    else:
        username = None

    return render_template("login.html", username=username)

# this route handle step 4 of the authentication workflow
@app.route("/login", methods=["POST"])
def process_login_form():
    # plumbing code for us to query DB
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()

    # create our redirect to homepage response
    response = redirect("/")

    # find user row in users table that matches the submitted username
    cursor.execute("""
        SELECT id, password_hash
        FROM users
        WHERE username = %s
        LIMIT 1
    """, (request.form.get("username"),))
    user = cursor.fetchone()
    if not user:
        return response

    # verify that the password submitted by the user matches
    # the one in our DB
    encoded_password = request.form.get("password").encode()
    user_id, hashed_password = user
    if bcrypt.checkpw(encoded_password, hashed_password.encode()):
        session["user_id"] = user_id

    return response

@app.route("/logout")
def logout():
    # ask the browser to delete the session cookie
    # after which the browser will NOT send cookie to flask
    # hence flask cannot lookup the user in our DB
    session.pop("user_id", None)

    return redirect("/")
    

if __name__ == "__main__":
    app.run(debug=True)