import os
import psycopg2
import bcrypt
from flask import Flask, request, redirect, render_template, session


# get DATABASE_URL value from environment,
# if the value is NOT found, then use 'dbname=food_truck'
DATABASE_URL = os.environ.get('DATABASE_URL', 'dbname=transformer_store')

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

@app.route('/cart', methods=['post'])
def cart(): 
    name = request.form.get('name')
    print(name)
    return render_template("cart.html")


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
    

if __name__ == "__main__":
    app.run(debug=True)